import sys
import logging
from loguru import logger

format = ("<green>{time:YYYY-MMDD HH:mm:ss.SSS}</green> | {extra[namespace]} | "
          "<level>{level: <8}</level> | "
          "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")


logger.add("file_A1.log", )
logger.add("file_A1.log", )
logger.add("file_A1.log", )
logger.add("file_A1.log", )
logger.add("file_A1.log", )
logger.add("file_A1.log", )
# logger.add(('file_B1.log'))


logger.info('hahha2')




