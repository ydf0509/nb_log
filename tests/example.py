from nb_log import get_logger

logger =get_logger('lalala')

for i in range(10000000):
    logger.debug(f'绿色{i}')
    logger.info('蓝色')
    logger.warning('黄色')
    logger.error('粉红色')
    logger.critical('紫红色')



