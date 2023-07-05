from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError
import asyncio

with workflow.unsafe.imports_passed_through():
    from activities import UserSentimentInput, UserSentimentOutput, get_user_sentiment, get_location, get_available_task_queue, Signal


@workflow.defn
class ReviewProcessingWorkflow:
    def __init__(self) -> None:
        self._pending_user_sentiment: asyncio.Queue[UserSentimentInput] = asyncio.Queue()
        self._exit = False   

    @workflow.run 
    async def run(self, input: UserSentimentInput) -> UserSentimentOutput:
        # Setup a timer to fail workflow if timer fires
        timeout = 300
        try:
            result = await asyncio.wait_for(workflow_impl(self, input), timeout)
        except TimeoutError as e:
            raise ApplicationError(f"Workflow timeout of {timeout} seconds reached") from e 

        return result      

    @workflow.query
    def locations(self) -> list[str]:
        return self._locations

    @workflow.query
    def results(self) -> UserSentimentOutput:
        return self._results

    @workflow.signal
    async def pending_user_sentiment(self, info: Signal) -> None:
        await self._pending_user_sentiment.put(info)

    @workflow.signal
    def exit(self) -> None:
        self._exit = True              

async def workflow_impl(self, input: UserSentimentInput) -> UserSentimentOutput:
    self._results = UserSentimentOutput
    self._locations = list[str]

    unique_worker_task_queue = await workflow.execute_activity(
        activity=get_available_task_queue,
        start_to_close_timeout=timedelta(seconds=10),
    )

    workflow.logger.info(f"Matching workflow to worker {unique_worker_task_queue}")

    locations = await workflow.execute_activity(
        get_location,
        input,
        task_queue=unique_worker_task_queue,
        start_to_close_timeout=timedelta(seconds=60),                  
    )

    self._locations = locations   

    # Wait for queue item or exit
    await workflow.wait_condition(
        lambda: not self._pending_user_sentiment.empty() or self._exit
    )

    # Drain and process queue
    while not self._pending_user_sentiment.empty(): 
        result = await workflow.execute_activity(
            get_user_sentiment,
            self._pending_user_sentiment.get_nowait(),
            task_queue=unique_worker_task_queue,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),                  
        )
        self._results = result

        return result    