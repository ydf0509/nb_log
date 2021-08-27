"""
只要满足3个条件
1.文件日志
2.文件日志按大小或者时间切割
3.多进程写入同一个log文件，可以是代码内部multiprocess.Process启动测试，
  也可以代码内容本身不用多进程但把脚本反复启动运行多个来测试。

把切割大小或者切割时间设置的足够小就很容易频繁必现，平时有的人没发现是由于把日子设置成了1000M切割或者1天切割，
自测时候只随便运行一两下就停了，日志没达到需要切割的临界值，所以不方便观察到切割日志文件的报错。

这里说的是多进程文件日志切割报错，有的人老说多线程，简直是服了。
面试时候把多进程和多线程区别死记硬背 背的一套一套很溜的，结果实际运用连进程和线程都不分。
"""
from logging.handlers import  RotatingFileHandler
import logging
from multiprocessing import Process
from threading import Thread

logger = logging.getLogger('test_raotating_filehandler')

logger.addHandler(RotatingFileHandler(filename='testratationg.log',maxBytes=1000 *100,backupCount=10))

def f():
    while 1:
        logger.warning('这个代码会疯狂报错，因为设置了100Kb就切割并且在多进程下写入同一个日志文件'*20)

if __name__ == '__main__':
    for _ in range(10):
        Process(target=f).start()  # 反复强调的是 文件日志切割并且多进程写入同一个文件，会疯狂报错
        # Thread(target=f).start()  # 多线程没事，所有日志handler无需考虑多线程是否安全，说的是多进程文件日志切割不安全，你老说多线程干嘛？