import time

import nb_log

logger = nb_log.get_logger('name1', is_use_loguru_stream_handler=True, log_level_int=10,log_filename='testloguru_file.log',log_file_handler_type=7)
logger2 = nb_log.get_logger('name2', is_use_loguru_stream_handler=True, log_level_int=10,log_filename='testloguru_file2.log',log_file_handler_type=7)

for i in range(10000000000):
    logger.debug(f'loguru debug 111111')
    logger2.debug(f'loguru debug 222222')

    logger.info('loguru info 111111')
    logger2.info('loguru info 222222')

    logger.warning('loguru warn 111111')
    logger2.warning('loguru warn 22222 ')

    logger.error('loguru err 1111111')
    logger2.error('loguru err 2222222')

    logger.critical('loguru critical 111111')
    logger2.critical('loguru caritical 222222')

    time.sleep(1)

# import requests
#
# nb_log.get_logger('', is_use_loguru_stream_handler=True)
#
# requests.get('http://www.baidu.com')


# time.sleep(100000)