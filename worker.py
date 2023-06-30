import asyncio
from temporalio.worker import Worker
import os

from activities import (
    get_best_label
)

from client import get_worker_client
from workflow import InferenceWorkflow


async def main():
    client = await get_worker_client()

    worker = Worker(
        client,
        task_queue=os.getenv("TEMPORAL_TASK_QUEUE"),
        workflows=[InferenceWorkflow],
        activities=[
            get_best_label
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())