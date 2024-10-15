import time

import logging
import nb_log
from nb_log import CompatibleLogger


class LogException(Exception):
    """
    自动记录日志的异常，抛出异常不需要单独再写日志
    """
    logger: logging.Logger = None
    is_record_log: bool = True

    def __init__(self, err_msg, *, logger: logging.Logger = None, is_record_log: bool = True):  # real signature unknown
        logger = logger or self.__class__.logger
        self.err_msg = err_msg
        if logger and (is_record_log or self.__class__.is_record_log):
            logger.error(self.err_msg, extra={'sys_getframe_n': 3})

    def __str__(self):
        return str(self.err_msg)


if __name__ == '__main__':
    loggerx = nb_log.LogManager('log_exc', logger_cls=CompatibleLogger).get_logger_and_add_handlers(log_filename='log_exc.log')

    # try:
    #     raise LogException(['cccc', 222], logger=loggerx)
    # except Exception as e:
    #     print(e)
    # try:
    #     raise LogException('cccc', logger=loggerx)
    # except Exception as e:
    #     loggerx.exception(e)

    # print('aaaaaaaaaaaaaaaa')
    time.sleep(1)
    raise LogException(['cccc', 222], logger=loggerx)  #

    print('ok')
