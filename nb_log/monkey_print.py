# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/5/9 19:02
"""
Custom print patching - reassigns the built-in print function.
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
WORD_COLOR = nb_log_config_default.WHITE_COLOR_CODE


def stdout_write(msg: str):
    if sys.stdout:
        sys.stdout.write(msg)
        sys.stdout.flush()


def stderr_write(msg: str):
    '''When packaged as exe or running as Windows service, sys.stderr may be None'''
    if sys.stderr:
        sys.stderr.write(msg)
        sys.stderr.flush()
    else:
        stdout_write(msg)


print_wrtie_file_name = os.environ.get('PRINT_WRTIE_FILE_NAME', None) or nb_log_config_default.PRINT_WRTIE_FILE_NAME

print_file_writter = OsFileWritter(print_wrtie_file_name, log_path=nb_log_config_default.LOG_PATH,
                                   back_count=nb_log_config_default.LOG_FILE_BACKUP_COUNT, max_bytes=nb_log_config_default.LOG_FILE_SIZE * 1024 * 1024)


def _print_with_file_line(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2):
    args = (str(arg) for arg in args)  # REMIND Ensure all args are strings for join
    args_str = sep.join(args) + end
    # stdout_write(f'56:{file}')
    if file == sys.stderr:
        stderr_write(args_str)  # Keep original red error output for stderr (e.g. threading module errors).
        print_file_writter.write_2_file(args_str)
    elif file in [sys.stdout, None]:
        # Get the caller's file and line number
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
                stdout_write(f'\033[0;34m{now_str}  "{file_name}:{line}" -{fun}-[print]-  \033[0;{WORD_COLOR};44m{args_str[:-1]}\033[0m \033[0m\n')  # 36  93 96 94
            else:
                stdout_write(
                    f'\033[0;{WORD_COLOR};34m{now_str}  "{file_name}:{line}" -{fun}-[print]-  {args_str[:-1]}  \033[0m\n')  # 36  93 96 94
            # sys.stdout.write(f'\033[0;30;44m"{file_name}:{line}"  {time.strftime("%H:%M:%S")}  {"".join(args)}\033[0m\n')
        else:
            stdout_write(
                f'{now_str}  "{file_name}:{line}"  -{fun}-[print]- {args_str} ')
        print_file_writter.write_2_file(f'{now_str}  "{file_name}:{line}" -[print]-{fun}- {args_str} ')  # 36  93 96 94
    else:  # For file objects like StringIO (used by traceback.print_exception), redirect content to preserve exception stack traces.
        print_raw(args_str, sep=sep, end=end, file=file)
        print_file_writter.write_2_file(args_str)


# noinspection PyProtectedMember,PyUnusedLocal,PyIncorrectDocstring,DuplicatedCode
def nb_print(*args, sep=' ', end='\n', file=None, flush=True):
    """
    Enhanced print with color, file/line info, and clickable navigation.
    :param x:
    :return:
    """
    _print_with_file_line(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)


# noinspection PyPep8,PyUnusedLocal
def print_exception(etype, value, tb, limit=None, file=None, chain=True):
    """
    Prevents two clickable links per line which would cause the IDE to not recognize the second one.
    Primarily for print_exception, which is called by logging.exception.

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

_patched_pids = set()

def patch_print():
    """
    Python has several namespaces: locals, globals, and builtins.
    Variables declared inside functions belong to locals, while module-level definitions belong to globals.

    https://codeday.me/bug/20180929/266673.html

    :return:
    """
    current_pid = os.getpid()
    if current_pid in _patched_pids:
        return
    _patched_pids.add(current_pid)
    try:
        __builtins__.print = nb_print
    except AttributeError:
        """
        <class 'AttributeError'>
        'dict' object has no attribute 'print'
        """
        # noinspection PyUnresolvedReferences
        __builtins__['print'] = nb_print
    # traceback.print_exception = print_exception  # Handled by separate file type check for StringIO, no need for this.


def common_print(*args, sep=' ', end='\n', file=None):
    args = (str(arg) for arg in args)
    args = (str(arg) for arg in args)  # REMIND Ensure all args are strings for join
    if file == sys.stderr:
        stderr_write(sep.join(args) + end)  # Keep original red error output for stderr.
    else:
        stdout_write(sep.join(args) + end)


def reverse_patch_print():
    """
    Reverse the monkey-patch and restore the original print function.
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
    # Only print when called from the main process
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
