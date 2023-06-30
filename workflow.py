from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import InferenceInput, get_best_label


@workflow.defn
class InferenceWorkflow:
    @workflow.run
    async def run(self, input: InferenceInput):      

        output = await workflow.execute_activity(
            get_best_label,
            input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
            ),                  
        )

        return output 