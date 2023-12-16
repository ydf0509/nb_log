import nb_log

logger = nb_log.get_logger('name1', is_use_loguru_stream_handler=True, log_level_int=10)
logger2 = nb_log.get_logger('name2', is_use_loguru_stream_handler=True, log_level_int=10)

logger.debug(f'loguru debug ')
logger2.debug(f'loguru2 debug')

logger.info('loguru info ')
logger2.info('loguru2 info ')

logger.warning('loguru warm')
logger2.warning('loguru2 warm ')

logger.error('loguru err ')
logger2.error('loguru2 err')

logger.critical('loguru critical')
logger2.critical('loguru2 caritical ')

import requests

nb_log.get_logger('urllib3', is_use_loguru_stream_handler=True)

requests.get('http://www.baidu.com')