import logging

from nb_log import get_logger,LogManager


LogManager('RedisDistributedLockContextManager').preset_log_level(30)

logger = get_logger('RedisDistributedLockContextManager')


logger.debug('这句话打印不出来了.RedisDistributedLockContextManager 命名空间的日志锁定了 warnning级别,不可更改')

LogManager('').preset_log_level(20)
get_logger('root').info('infoging')

logging.RootLogger
print(logging.getLogger(''))
print(logging.getLogger('root'))
print(logging.getLogger(None))

print(logging.getLogger() == logging.getLogger('root'))
