import time
import asyncio
import threading

import nb_log.global_except_hook

nb_log.get_logger(None)


def f():
    time.sleep(5)
    raise Exception('errorxixixi')

async def af():
    await asyncio.sleep(5)
    raise Exception('errorxixixi22')

# threading.Thread(target=f).start()
# loop = asyncio.new_event_loop()
# loop.create_task(af())


time.sleep(7)

raise Exception('bbb')
