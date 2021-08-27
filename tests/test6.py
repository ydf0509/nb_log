from nb_log import get_logger


logger = get_logger('abcde',log_filename='abcde.log',log_file_handler_type=4)


for i in range(1000000000):
    logger.info('hello')

