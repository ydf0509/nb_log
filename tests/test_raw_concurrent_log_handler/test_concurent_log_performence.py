import logging
import time

import concurrent_log_handler

logger = logging.getLogger("MyExample")
logger.setLevel(logging.DEBUG)  # optional to set this level here

handler = concurrent_log_handler.ConcurrentTimedRotatingFileHandler(
    filename="/pythonlogs/logger_fj.log", mode="a", maxBytes=1000 * 1000 * 100, backupCount=6,when='d',
)

handler = logging.FileHandler(
    filename="/pythonlogs/logger_fj.log", mode="a",
)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

print(time.strftime('%Y_%m_%d %H:%M:%S'))
for i in range(100000):
    logger.info(f'abcdefgfgbfgddhfgdhjfgjfghkjhkggj {i}')
print(time.strftime('%Y_%m_%d %H:%M:%S'))