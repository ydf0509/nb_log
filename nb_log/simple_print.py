import atexit
import os
import queue
import sys
import threading
import time
import multiprocessing

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



def _sprint(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2, ):
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    args_str = sep.join(args) + end
    # stdout_write(f'56:{file}')
    if file == sys.stderr:
        stderr_write(args_str)  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    elif file in [sys.stdout, None]:
        # 获取被调用函数在被调用时所处代码行数
        fra = sys._getframe(sys_getframe_n)
        line = fra.f_lineno
        file_name = fra.f_code.co_filename
        fun = fra.f_code.co_name
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        msg = f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}"  - {fun} - {args_str}'
        stdout_write(msg)
    else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
        print_raw(args_str, sep=sep, end=end, file=file)


def sprint(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2, only_print_on_main_process=False):
    if only_print_on_main_process:
        if multiprocessing.process.current_process().name == 'MainProcess':
            _sprint(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)
    else:
        _sprint(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=sys_getframe_n)


if __name__ == '__main__':
    str1 = 'O(∩_∩)O哈哈' * 40
    t1 = time.time()
    for i in range(10000):
        sprint(str1)

    print(time.time() - t1)
