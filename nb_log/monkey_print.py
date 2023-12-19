# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/5/9 19:02
"""
不直接给print打补丁，自己重新赋值。

"""
import multiprocessing
import os
import sys
import time
import traceback
from nb_log import nb_log_config_default
# from nb_log.file_write import PrintFileWritter
from nb_log.rotate_file_writter import OsFileWritter

print_raw = print
WORD_COLOR = 37


def stdout_write(msg: str):
    if sys.stdout:
        sys.stdout.write(msg)
        sys.stdout.flush()


def stderr_write(msg: str):
    if sys.stderr:
        sys.stderr.write(msg)
        sys.stderr.flush()
    else:
        stdout_write(msg)


print_wrtie_file_name = os.environ.get('PRINT_WRTIE_FILE_NAME', None) or nb_log_config_default.PRINT_WRTIE_FILE_NAME

print_file_writter = OsFileWritter(print_wrtie_file_name, log_path=nb_log_config_default.LOG_PATH,
                                   back_count=nb_log_config_default.LOG_FILE_BACKUP_COUNT, max_bytes=nb_log_config_default.LOG_FILE_SIZE * 1024 * 1024)


def _print_with_file_line(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2):
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    args_str = sep.join(args) + end
    # stdout_write(f'56:{file}')
    if file == sys.stderr:
        stderr_write(args_str)  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
        print_file_writter.write_2_file(args_str)
    elif file in [sys.stdout, None]:
        # 获取被调用函数在被调用时所处代码行数
        fra = sys._getframe(sys_getframe_n)
        line = fra.f_lineno
        file_name = fra.f_code.co_filename
        fun = fra.f_code.co_name
        now_str= time.strftime("%Y-%m-%d %H:%M:%S")
        # mtime = time.gmtime()
        # now_str = f'{mtime.tm_year}-{mtime.tm_mon}-{mtime.tm_mday} {mtime.tm_hour}:{mtime.tm_min}:{mtime.tm_sec}'
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        if nb_log_config_default.DEFAULUT_USE_COLOR_HANDLER:
            if nb_log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
                stdout_write(
                    f'\033[0;34m{now_str}  "{file_name}:{line}" -{fun}-[print]-  \033[0;{WORD_COLOR};44m{args_str[:-1]}\033[0m \033[0m\n')  # 36  93 96 94
            else:
                stdout_write(
                    f'\033[0;{WORD_COLOR};34m{now_str}  "{file_name}:{line}" -{fun}-[print]-  {args_str[:-1]}  \033[0m\n')  # 36  93 96 94
            # sys.stdout.write(f'\033[0;30;44m"{file_name}:{line}"  {time.strftime("%H:%M:%S")}  {"".join(args)}\033[0m\n')
        else:
            stdout_write(
                f'{now_str}  "{file_name}:{line}"  -{fun}-[print]- {args_str} ')
        print_file_writter.write_2_file(f'{now_str}  "{file_name}:{line}" -[print]-{fun}- {args_str} ')  # 36  93 96 94
    else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
        print_raw(args_str, sep=sep, end=end, file=file)
        print_file_writter.write_2_file(args_str)


# noinspection PyProtectedMember,PyUnusedLocal,PyIncorrectDocstring,DuplicatedCode
def nb_print(*args, sep=' ', end='\n', file=None, flush=True):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    _print_with_file_line(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)


# noinspection PyPep8,PyUnusedLocal
def print_exception(etype, value, tb, limit=None, file=None, chain=True):
    """
    避免每行有两个可跳转的，导致第二个可跳转的不被ide识别。
    主要是针对print_exception，logging.exception里面会调用这个函数。

    # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断sys.stderr sys.stdout 以外的情况了，解决了，不需要用到p rint_exception。

    :param etype:
    :param value:
    :param tb:
    :param limit:
    :param file:
    :param chain:
    :return:
    """
    if file is None:
        file = sys.stderr
    for line in traceback.TracebackException(
        type(value), value, tb, limit=limit).format(chain=chain):
        # print(line, file=file, end="")
        if file != sys.stderr:
            stderr_write(f'{line} \n')
        else:
            stdout_write(f'{line} \n')


# print = nb_print

def patch_print():
    """
    Python有几个namespace，分别是

    locals

    globals

    builtin

    其中定义在函数内声明的变量属于locals，而模块内定义的函数属于globals。


    https://codeday.me/bug/20180929/266673.html   python – 为什么__builtins__既是模块又是dict

    :return:
    """
    try:
        __builtins__.print = nb_print
    except AttributeError:
        """
        <class 'AttributeError'>
        'dict' object has no attribute 'print'
        """
        # noinspection PyUnresolvedReferences
        __builtins__['print'] = nb_print
    # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断，解决了，不要加这个。


def common_print(*args, sep=' ', end='\n', file=None):
    args = (str(arg) for arg in args)
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        stderr_write(sep.join(args) + end)  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    else:
        stdout_write(sep.join(args) + end)


def reverse_patch_print():
    """
    提供一个反猴子补丁，恢复print原状
    :return:
    """
    # try:
    #     __builtins__.print = common_print
    # except AttributeError:
    #     __builtins__['print'] = common_print

    try:
        __builtins__.print = print_raw
    except AttributeError:
        __builtins__['print'] = print_raw


def is_main_process():
    return multiprocessing.process.current_process().name == 'MainProcess'


# noinspection DuplicatedCode
def only_print_on_main_process(*args, sep=' ', end='\n', file=None, flush=True):
    # 获取被调用函数在被调用时所处代码行数
    if is_main_process():
        _print_with_file_line(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)


if __name__ == '__main__':
    print('before patch')
    patch_print()
    print(0)
    nb_print(123, 'abc')
    print(456, 'def')
    print('http://www.baidu.com')

    reverse_patch_print()
    common_print('hi')

    import logging

    try:
        1 / 0
    except Exception as e:
        logging.exception(e)
