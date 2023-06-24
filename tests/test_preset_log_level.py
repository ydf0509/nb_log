from multiprocessing import Process

from nb_log import get_logger,LogManager


LogManager('abcd').preset_log_level(10)


def f():
    logger = get_logger('abcd',log_level_int=10)
    logger.debug('哈')


if __name__ == '__main__':
    Process(target=f).start()