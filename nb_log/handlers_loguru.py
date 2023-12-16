import logging

import sys


class LoguruStreamHandler(logging.Handler):
    """
    loguru 的 控制台效果
    """

    def __init__(self, logger_name):
        logging.Handler.__init__(self)
        from loguru import logger
        # print(logger._core.handlers)
        try:
            logger.remove(0)
        except ValueError as e:
            pass
            # print(e)
        format = ("<green>{time:YYYY-MMDD HH:mm:ss.SSS}</green> | {extra[namespace]} | "
                  "<level>{level: <8}</level> | "
                  "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
        logger.add(sys.stdout, filter=lambda record: record["extra"]["namespace"] == logger_name, format=format)
        self.logurux = logger.bind(namespace=logger_name)
        options_list = list(self.logurux._options)
        options_list[1] = 6  # 转化是为了显示实际的日志发生处，而不是封装loguru的emit方法处。
        self.logurux._options = tuple(options_list)
        # print(logger._core.handlers)

    def emit(self, record):
        level_str = logging._levelToName[record.levelno]
        # self.logurux.log(level_str, self.format(record))
        self.logurux.log(level_str,record.getMessage())
