import nb_log

"""
禁止使用此种错误方式来封装 nb_log ，因为跳转到的日志地方跳转到你的这个类了，而不是精确跳转到 logger.debug/info()  的地方
并且日志的name 千万不要固定死了，多命名空间才是日志精髓。
所有日志只能写入到mylog.log文件中，不能写入不同的文件
"""
class LogUtil:
    def __init__(self):
        self.logger = nb_log.get_logger('xx',log_filename='mylog.log')

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
    print('日志命名固定死了，没有多实例单独控制很差劲。所有日志只能写入到mylog.log文件中，不能写入不同的文件')
    LogUtil().debug('不能跳转到本行，跳转到工具类去了')
    LogUtil().info('不能跳转到本行，跳转到工具类去了')
    LogUtil().warning('不能跳转到本行，跳转到工具类去了')
    LogUtil().error('不能跳转到本行，跳转到工具类去了')
    LogUtil().critical('不能跳转到本行，跳转到工具类去了')