"""
这个文件是个错误例子，多进程还想按大小切割文件，由于在达到指定大小瞬间，a进程切割了文件，b进程不到文件句柄了。
只有nb_log才能解决多进程文件切割，实现难度很高。

说的是多进程下不行，多线程任何handler都是安全的。说的是多进程不行不是多线程不行！！！！
此demo会疯狂报错。
"""
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