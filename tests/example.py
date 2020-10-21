from nb_log import get_logger

logger =get_logger('lalala',log_filename='aaa.log',
                   is_use_watched_file_handler_instead_of_custom_concurrent_rotating_file_handler=False)

for i in range(10000):
    logger.debug(f'绿色{i}')
    logger.info('蓝色')
    logger.warning('黄色yello')
    logger.error('粉红色')
    logger.critical('紫红色')



