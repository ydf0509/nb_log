import nb_log

class LogUtil:
    def __init__(self):
        self.logger = nb_log.get_logger('xx')

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

if __name__ == '__main__':
    print('日志命名固定死了，没有多实例单独控制很差劲。')
    LogUtil().debug('不能跳转到本行，跳转到工具类去了')
    LogUtil().info('不能跳转到本行，跳转到工具类去了')
    LogUtil().warning('不能跳转到本行，跳转到工具类去了')
    LogUtil().error('不能跳转到本行，跳转到工具类去了')
    LogUtil().critical('不能跳转到本行，跳转到工具类去了')