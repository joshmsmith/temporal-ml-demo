from activities import InferenceInput
from workflow import InferenceWorkflow
import uuid
from client import get_client
import asyncio
 
async def main():
    id = str(uuid.uuid4().int)[:6]

    input = InferenceInput(
        sequence = "This is terrible service",
        candidate_labels = ['happy', 'sad', 'angry', 'neutral']
    )  

    client = await get_client()

    booking_workflow = await client.start_workflow(
        InferenceWorkflow.run,
        input,
        id=f'inference-{id}',
        task_queue="activity_sticky_queue-distribution-queue",
    )

    print(booking_workflow)

if __name__ == "__main__":
    asyncio.run(main())
