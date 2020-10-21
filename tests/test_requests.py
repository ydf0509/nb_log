import requests
from nb_log import get_logger

logger = get_logger('urllib3', log_filename='urllib3.log', formatter_template=8,
                    is_use_watched_file_handler_instead_of_custom_concurrent_rotating_file_handler=True)
requests.get('http://www.baidu.com')
logger.debug(11, extra={'c': 5, 'd': 6})
logger.info(22)
logger.warning(33)
logger.error(44)
logger.critical(55,extra=dict(f=7,g=8,h=9))

logger.debug('哈哈哈哈', extra=dict(a=1, b=2))
try:
    1 / 0
except Exception as e:
    logger.exception('错误了')
