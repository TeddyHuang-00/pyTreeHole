import asyncio
import datetime
import json
import logging
from typing import List

from treehole import Hole, TreeHoleClient

secrets = json.load(open("./secrets.json"))
token = secrets["token"]
client = TreeHoleClient(token)

logger = logging.getLogger("sample_async")
logger.setLevel(logging.DEBUG)


async def consumer(todo_queue: asyncio.Queue, done_queue: asyncio.Queue):
    logger.info(f"Consumer started at {datetime.datetime.now()}")
    while True:
        if todo_queue.empty():
            await asyncio.sleep(1.0)
            continue
        hole_id = await todo_queue.get()
        hole = await client.get_hole_async(hole_id)
        if hole is not None:
            logger.debug(f"Got hole {hole_id}")
            await done_queue.put(hole)
        else:
            logger.debug(f"Failed to get hole {hole_id}")
        todo_queue.task_done()
        # This is important to prevent the server from being overwhelmed (503 response)
        await asyncio.sleep(2.0)


async def producer(
    target_time: datetime.datetime, todo_queue: asyncio.Queue, done_queue: asyncio.Queue
):
    logger.info(f"Producer started at {datetime.datetime.now()}")
    target_timestamp = int(target_time.timestamp())
    logger.debug(f"Targeting time at {target_time}")
    holes = await client.get_holes_async()
    assert holes is not None
    logger.info(f"Found {len(holes)} holes")
    assert holes[0].pid
    index: int = holes[0].pid
    for idx in range(index, index - len(holes), -1):
        todo_queue.put_nowait(idx)
        await asyncio.sleep(0.1)
    index -= len(holes)
    results = []
    while not done_queue.empty() or not todo_queue.empty():
        hole: Hole = await done_queue.get()
        done_queue.task_done()
        assert hole.timestamp
        if hole.timestamp > target_timestamp:
            logger.debug(
                f"Receive hole {hole.pid} @ {datetime.datetime.fromtimestamp(hole.timestamp)}"
            )
            await todo_queue.put(index)
            index -= 1
            results.append(hole)
        else:
            logger.debug(
                f"Reject hole {hole.pid} @ {datetime.datetime.fromtimestamp(hole.timestamp)}"
            )
    done_queue.put_nowait(results)
    return


async def main(time: datetime.datetime) -> List[Hole]:
    if time > datetime.datetime.now():
        raise ValueError("time should be in the past")
    logger.debug(f"Starting main at {datetime.datetime.now()}")
    todo_queue = asyncio.Queue()
    done_queue = asyncio.Queue()
    workers = []
    for i in range(10):
        logger.debug(f"Starting worker {i} at {datetime.datetime.now()}")
        worker_task = asyncio.create_task(consumer(todo_queue, done_queue))
        workers.append(worker_task)
    logger.debug(f"Starting producer at {datetime.datetime.now()}")
    producer_task = asyncio.create_task(producer(time, todo_queue, done_queue))
    await asyncio.sleep(5)
    logger.debug(f"Waiting for consumers to finish...")
    await todo_queue.join()
    logger.debug(f"Cancelling workers at {datetime.datetime.now()}")
    for worker in workers:
        worker.cancel()
    logger.debug(f"Waiting for workers to be canceled...")
    await asyncio.gather(*workers, return_exceptions=True)
    return await done_queue.get()


if __name__ == "__main__":
    results = asyncio.run(
        # 获取当前时间前十分钟的所有洞
        main(datetime.datetime.today() - datetime.timedelta(minutes=10))
    )
    json.dump(
        results,
        open("tmp.results.json", "w"),
        ensure_ascii=False,
        default=lambda x: x.data,
    )
