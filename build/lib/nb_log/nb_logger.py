import sys
import os
import traceback
import io
import logging
from logging import _srcfile

'''
新增的 NbLogger 类，继承自内置 logging.Logger，
主要作用是可以改变 sys._getframe 深度，  
目的是 如果用户自己使用代码模式封装了日志类，在自己的类中又多此一举实现 debug info warning error critical 打印日志的方法， 
用户在使用 用户自己类.debug() 时候 ，导致记录日志的行号是用户封装这几个方法的地方，而不是实际打印日志的地方，不方便定位日志是从哪里打印的。
'''

'''
from nb_log import get_logger


class 废物日志类:
    def __init__(self,name):
        self.logger = get_logger(name, log_filename='废物日志.log')

    def debug(self, msg):
        self.logger.debug(msg, extra={'sys_getframe_n': 3})  # 第 x1 行

    def info(self, msg):
        self.logger.info(msg, extra={'sys_getframe_n': 3})  # 第 x2 行


废物日志类('命名空间1').info('啊啊啊啊')  # 第y行
'''

'''
有的人手痒，非要封装nb_log,那么封装时候调用原生日志的 info() 务必要传入  extra={'sys_getframe_n': 3}
如果你不传递 extra={'sys_getframe_n': 3} ，那么 废物日志类().info('啊啊啊啊') ，显示是第 x2 行打印的日志，而不是第 y行打印的日志。
'''

class NbLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """

        sys_getframe_n =2
        if extra and 'sys_getframe_n' in extra:
            sys_getframe_n = extra['sys_getframe_n']
            extra.pop('sys_getframe_n')
        sinfo = None
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info,sys_getframe_n)  # 这个改了，加了个入参。
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                 exc_info, func, extra, sinfo)
        self.handle(record)

    def findCaller(self, stack_info=False,sys_getframe_n =2):
        """
        主要是改了这个，使得文件和行号变成用户本身的打印日志地方，而不是封装日志的地方。
        :param stack_info:
        :param sys_getframe_n: 新增的入参。
        :return:
        """
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = sys._getframe(sys_getframe_n)   # 这行改了。
        # f = sys._getframe(3)
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

