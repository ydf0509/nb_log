import logging
import typing
from logging import Formatter, LogRecord


class ContextFormatter(Formatter):
    def __init__(self, *args, get_context_field_fun: typing.Callable = None, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.get_context_field_fun = get_context_field_fun

    def formatMessage(self, record: LogRecord):
        context_id = ''
        if self.get_context_field_fun:
            context_id = self.get_context_field_fun()
        setattr(record, 'context_id', context_id)
        return self._style.format(record)


if __name__ == '__main__':
    def f():
        return 'aaaaaa6666'


    logger = logging.getLogger('abcd')
    sh = logging.StreamHandler()
    formatter = ContextFormatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(context_id)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
        "%Y-%m-%d %H:%M:%S", get_context_field_fun=None)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    logger.info('哈哈哈哈')
