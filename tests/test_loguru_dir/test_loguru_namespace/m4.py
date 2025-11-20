

from loguru import logger


import sys

logger.remove()

# 1. 你的日志：INFO 以上
logger.add(sys.stderr, level="INFO", filter=lambda r:  r["name"].startswith("m3"))
logger.add(sys.stderr, level="INFO", filter=lambda r: not r["name"].startswith("m3"))

import m3


logger.info('m4 info')
