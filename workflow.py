from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import UserSentimentInput, get_user_sentiment, get_available_task_queue


@workflow.defn
class ReviewProcessingWorkflow:
    @workflow.run
    async def run(self, input: UserSentimentInput):      
        unique_worker_task_queue = await workflow.execute_activity(
            activity=get_available_task_queue,
            start_to_close_timeout=timedelta(seconds=10),
        )

        workflow.logger.info(f"Matching workflow to worker {unique_worker_task_queue}")

        #output = await workflow.execute_activity(
        #    get_best_label,
        #    input,
        #    task_queue=unique_worker_task_queue,
        #    start_to_close_timeout=timedelta(seconds=60),
        #    retry_policy=RetryPolicy(
        #        maximum_attempts=3,
        #    ),                  
        #)

        result = await workflow.execute_activity(
            get_user_sentiment,
            input,
            task_queue=unique_worker_task_queue,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),                  
        )        

        return result 