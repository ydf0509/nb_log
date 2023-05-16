

"""
这个文件是个错误例子，多进程还想按时间切割文件，由于在达到指定大小瞬间，a进程切割了文件，b进程不到文件句柄了。
只有nb_log才能解决多进程文件切割，实现难度很高。
"""
from logging.handlers import  TimedRotatingFileHandler
import logging
from multiprocessing import Process

logger = logging.getLogger('test_raotating_filehandler')

logger.addHandler(TimedRotatingFileHandler(filename='test_timed_ratationg.log',when='S',interval=5))

def f():
    while 1:
        logger.warning('测试多进程按时间切片出错不')

if __name__ == '__main__':
    for _ in range(10):
        Process(target=f).start()