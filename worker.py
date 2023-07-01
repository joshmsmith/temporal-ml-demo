import asyncio
import random
from typing import List
from uuid import UUID

from temporalio import activity
from temporalio.worker import Worker

interrupt_event = asyncio.Event()

from activities import get_best_label, get_user_sentiment
from client import get_worker_client
from workflow import ReviewProcessingWorkflow

async def main():
    random.seed(667)

    # Create random task queues and build task queue selection function
    task_queue: str = f"activity_sticky_queue-host-{UUID(int=random.getrandbits(128))}"

    # Randomly assign job to a task queue
    @activity.defn(name="get_available_task_queue")
    async def get_task_queue() -> str:
        return task_queue

    # Load client
    client = await get_worker_client()

    # Run a worker to distribute the workflows
    run_futures = []
    handle = Worker(
        client,
        task_queue="activity_sticky_queue-distribution-queue",
        workflows=[ReviewProcessingWorkflow],
        activities=[get_task_queue],
    )
    run_futures.append(handle.run())
    print("Base worker started")

    # Run unique task queue for file processing on this host
    handle = Worker(
        client,
        task_queue=task_queue,
        activities=[
        #    get_best_label,
            get_user_sentiment,
        ],
    )

    run_futures.append(handle.run())

    print(f"Worker {task_queue} started")
    print("All workers started, ctrl+c to exit")

    # Wait until interrupted
    await asyncio.gather(*run_futures)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())
        print("\nShutting down workers")

        