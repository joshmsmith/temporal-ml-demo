from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import InferenceInput, get_best_label, get_available_task_queue, update_rating


@workflow.defn
class InferenceWorkflow:
    @workflow.run
    async def run(self, input: InferenceInput):      
        unique_worker_task_queue = await workflow.execute_activity(
            activity=get_available_task_queue,
            start_to_close_timeout=timedelta(seconds=10),
        )

        workflow.logger.info(f"Matching workflow to worker {unique_worker_task_queue}")

        output = await workflow.execute_activity(
            get_best_label,
            input,
            task_queue=unique_worker_task_queue,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),                  
        )

        await workflow.execute_activity(
            update_rating,
            task_queue=unique_worker_task_queue,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),                  
        )        

        return output 