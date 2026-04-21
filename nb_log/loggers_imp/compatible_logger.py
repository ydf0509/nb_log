import sys
import os
import traceback
import io
import logging
from logging import _srcfile

'''
CompatibleLogger class, inherits from the built-in logging.Logger.
Its main purpose is to allow customizing sys._getframe depth,
so that when users wrap the logger class with their own debug/info/warning/error/critical methods,
the logged file path and line number point to the actual call site, not the wrapper method.
'''

'''
from nb_log import get_logger


class MyLoggerWrapper:
    def __init__(self, name):
        self.logger = get_logger(name, _log_filename='my_logger.log')

    def debug(self, msg):
        self.logger.debug(msg, extra={'sys_getframe_n': 3})  # line x1

    def info(self, msg):
        self.logger.info(msg, extra={'sys_getframe_n': 3})  # line x2


MyLoggerWrapper('namespace1').info('hello')  # line y
'''

'''
When wrapping nb_log, always pass extra={'sys_getframe_n': 3} to debug/info/etc.
Without it, the logged line number would show line x2 (the wrapper) instead of line y (the actual call site).
'''


class CompatibleLogger(logging.Logger):

    """
    CompatibleLogger was originally developed for Python 3.7. Since Python 3.9, the official logging module
    added the `stacklevel` parameter to _log() and findCaller().

    This class provides the same functionality for Python 3.6/3.7/3.8 via the `sys_getframe_n` extra parameter,
    which serves the same purpose as `stacklevel` - adjusting the call stack depth to show
    the correct file/line when users wrap the debug/info/warning/error methods.
    """
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False,**kwargs):
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
                fn, lno, func, sinfo = self.findCaller(stack_info,sys_getframe_n)  # Modified: added sys_getframe_n parameter.
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
        Modified to resolve file/line to the actual log call site rather than the wrapper method.
        :param stack_info:
        :param sys_getframe_n: Custom stack frame depth parameter.
        :return:
        """
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = sys._getframe(sys_getframe_n)   # Modified: uses custom frame depth.
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

