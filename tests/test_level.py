import logging

from nb_log import get_logger
get_logger(None,log_level_int=logging.WARNING)
logger = get_logger('name2',log_level_int=logging.INFO)

logger.debug('debug的消息')
logger.info('info的消息')