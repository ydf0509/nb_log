import time

from nb_log import get_logger
from multiprocessing import Process

logger1 = get_logger('f1',log_filename='f1d.log',log_path='/pythonlogs',is_add_stream_handler=False,log_file_handler_type=6)
logger2 = get_logger('f2',log_filename='f2d.log',log_path='/pythonlogs',is_add_stream_handler=False)


def fun():
    for i in range(10000):
        logger1.warning(f'hi {i}')
        logger2.debug(f'hello {i}')


if __name__ == '__main__':
    Process(target=fun).start()
    Process(target=fun).start()

    time.sleep(10000)