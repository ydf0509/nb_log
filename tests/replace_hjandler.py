


import logging


class Myhandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        print(f'操作qt5控件写入 {record.msg}')

logger = logging.getLogger('abcd')

# logging.StreamHandler = Myhandler

logger.addHandler(logging.StreamHandler())

logger.warning('啊啊啊1')







