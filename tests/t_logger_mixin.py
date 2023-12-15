



from nb_log.log_manager import MetaTypeFileLogger,MetaTypeLogger



class Abcd(metaclass=MetaTypeLogger):
    @classmethod
    def clsf(cls):
        cls.logger.debug('aaaa')

    def f(self):
        self.logger.debug('bbbb')


if __name__ == '__main__':
    Abcd.clsf()
    Abcd().f()