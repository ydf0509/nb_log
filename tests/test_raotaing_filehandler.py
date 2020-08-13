from logging.handlers import  RotatingFileHandler
import logging
from multiprocessing import Process

logger = logging.getLogger('test_raotating_filehandler')

logger.addHandler(RotatingFileHandler(filename='testratationg.log',maxBytes=1000 *100,backupCount=10))

def f():
    while 1:
        logger.warning('测试多进程切片出错不')

if __name__ == '__main__':
    for _ in range(10):
        Process(target=f).start()