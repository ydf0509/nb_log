import logging

import nb_log

'''

有的笨瓜总是不能理解 logging.getLogger第一个入参name的作用和巨大好处，老是觉得需要实例化生成 logger 对象觉得麻烦，想开箱即用，那就满足这种人。
用from loguru import logger 这种日志，先不同模块或功能的日志设置不同级别，不同的模块写入不同的文件，非常麻烦不优雅。
但有的人完全不理解 日志命名空间的作用，只会抱怨nb_log的例子要他实例化不同name的logger麻烦，那就满足这种人，不用他手动实例化生成不同命名空间的logger。

import nb_log

nb_log.debug('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用debug函数，那就满足这种人')
nb_log.info('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用info函数，那就满足这种人')
nb_log.warning('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用warning函数，那就满足这种人')
nb_log.error('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用error函数，那就满足这种人')
nb_log.critical('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用critical函数，那就满足这种人')


loguru的用法是：
from loguru import logger
logger.debug(msg)

nb_log的用法是：
import nb_log
nb_log.debug(msg)

nb_log比loguru少了 from import那不是更简洁了吗？满足这种只知道追求简单的笨瓜。
'''

direct_logger = nb_log.LogManager('nb_log_direct', logger_cls=nb_log.CompatibleLogger).get_logger_and_add_handlers(log_filename='nb_log_direct.log')


def _convert_extra(kwargs: dict):
    """
    因为封装了原生logging的 debug info等方法，要显示实际的打印日志的文件和行号，需要把查找调用层级加大一级
    :param kwargs:
    :return:
    """
    extra = kwargs.get('extra', {})
    extra.update({"sys_getframe_n": 3})
    kwargs['extra'] = extra


def debug(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.error(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.exception(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.critical(msg, *args, **kwargs)
