from nb_log import LoggerMixin

class MyClass(LoggerMixin):
    def do_something(self):
        self.logger.info('这是一条信息日志')
        self.logger.warning('这是一条警告日志')
        self.logger.error('这是一条错误日志')

if __name__ == '__main__':
    obj = MyClass()
    obj.do_something()
