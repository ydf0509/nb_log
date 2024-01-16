import time
from loguru import logger as lg
import nb_log

logger = nb_log.get_logger('name1', is_use_loguru_stream_handler=True, log_filename='testloguru_file1.log', log_file_handler_type=7)
logger2 = nb_log.get_logger('name2', is_use_loguru_stream_handler=True, log_filename='testloguru_file2.log', log_file_handler_type=7)
logger_nb = nb_log.get_logger('name3', is_use_loguru_stream_handler=False, log_filename='testnblog_file3.log', log_file_handler_type=6)

for i in range(1):
    logger.debug(f'loguru debug 111111,写入文件  testloguru_file1.log')
    logger2.debug(f'loguru debug 222222,写入文件  testloguru_file2.log')
    logger_nb.debug(f'nb_log颜色模式,使用nb_log的文件写入方式')

    logger.info('loguru info 111111,写入文件  testloguru_file1.log')
    logger2.info('loguru info 222222,写入文件  testloguru_file2.log')
    logger_nb.info(f'nb_log颜色模式,使用nb_log的文件写入方式')

    logger.warning('loguru warn 111111,写入文件  testloguru_file1.log')
    logger2.warning('loguru warn 22222 ,写入文件  testloguru_file2.log')
    logger_nb.warning(f'nb_log颜色模式,使用nb_log的文件写入方式')

    logger.error('loguru err 1111111,写入文件  testloguru_file1.log')
    logger2.error('loguru err 2222222,写入文件  testloguru_file2.log')
    logger_nb.error(f'nb_log颜色模式,使用nb_log的文件写入方式')

    logger.critical('loguru critical 111111,写入文件  testloguru_file1.log')
    logger2.critical('loguru caritical 222222,写入文件  testloguru_file2.log')
    logger_nb.critical(f'nb_log颜色模式,使用nb_log的文件写入方式')

    time.sleep(1)

import requests

nb_log.get_logger('urllib3', is_use_loguru_stream_handler=True)

requests.get('http://www.baidu.com')


def errorf(x,y):
    try:
        x/y
    except Exception as e:
        logger.exception(e)


def error_req(url):
    try:
        requests.get(url)
    except Exception as e:
        lg.exception(e)

errorf(2,0)
error_req('http://www.baidu.com2')
time.sleep(100000)
