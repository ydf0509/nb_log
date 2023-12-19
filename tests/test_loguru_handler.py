import time

import nb_log

logger = nb_log.get_logger('name1', is_use_loguru_stream_handler=True, log_filename='testloguru_file1.log', log_file_handler_type=7)
logger2 = nb_log.get_logger('name2', is_use_loguru_stream_handler=True, log_filename='testloguru_file2.log', log_file_handler_type=7)

for i in range(1):
    logger.debug(f'loguru debug 111111,写入文件  testloguru_file1.log')
    logger2.debug(f'loguru debug 222222,写入文件  testloguru_file2.log')

    logger.info('loguru info 111111,写入文件  testloguru_file1.log')
    logger2.info('loguru info 222222,写入文件  testloguru_file2.log')

    logger.warning('loguru warn 111111,写入文件  testloguru_file1.log')
    logger2.warning('loguru warn 22222 ,写入文件  testloguru_file2.log')

    logger.error('loguru err 1111111,写入文件  testloguru_file1.log')
    logger2.error('loguru err 2222222,写入文件  testloguru_file2.log')

    logger.critical('loguru critical 111111,写入文件  testloguru_file1.log')
    logger2.critical('loguru caritical 222222,写入文件  testloguru_file2.log')

    time.sleep(1)

import requests

nb_log.get_logger('urllib3', is_use_loguru_stream_handler=True)

requests.get('http://www.baidu.com')

time.sleep(100000)
