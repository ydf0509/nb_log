import sys
import logging
from loguru import logger

format = ("<green>{time:YYYY-MMDD HH:mm:ss.SSS}</green> | {extra[namespace]} | "
          "<level>{level: <8}</level> | "
          "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

logger.remove()
logger.add("file_A.log", filter=lambda record: record["extra"]["namespace"] == "A", format=format)
logger.add(sys.stdout, filter=lambda record: record["extra"]["namespace"] == "A", format=format)

logger.add("file_B.log", filter=lambda record: record["extra"]["namespace"] == "B", format=format)
logger.add(sys.stdout, filter=lambda record: record["extra"]["namespace"] == "B", format=format)

logger_a = logger.bind(namespace="A")
logger_b = logger.bind(namespace="B")


def task_A():
    logger_a.info("Starting task A")
    logger_a.success("End of task A")


def task_B():
    logger_b.info("Starting task B")
    logger_b.success("End of task B")


task_A()
task_B()
