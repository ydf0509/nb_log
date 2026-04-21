import logging

import nb_log

'''
Convenience module for quick out-of-the-box logging without manually creating named loggers.
For users who prefer the simplicity of direct function calls (similar to loguru's interface).

Usage:
import nb_log
nb_log.debug('debug message')
nb_log.info('info message')
nb_log.warning('warning message')
nb_log.error('error message')
nb_log.critical('critical message')

Note: For production use, creating named loggers with get_logger() is strongly recommended
as it enables per-namespace log level control and separate file outputs.
'''

direct_logger = nb_log.LogManager('nb_log_direct', logger_cls=nb_log.CompatibleLogger).get_logger_and_add_handlers(log_filename='nb_log_direct.log')


def _convert_extra(kwargs: dict):
    """
    Adjusts the stack frame depth by one level to show the actual caller's file and line number
    instead of this wrapper module's location.
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
