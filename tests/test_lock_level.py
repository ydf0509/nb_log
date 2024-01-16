



from nb_log import get_logger,LogManager


LogManager('RedisDistributedLockContextManager').preset_log_level(30)

logger = get_logger('RedisDistributedLockContextManager')


logger.debug('这句话打印不出来了.RedisDistributedLockContextManager 命名空间的日志锁定了 warnning级别,不可更改')