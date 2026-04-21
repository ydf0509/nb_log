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
    args = (str(arg) for arg in args)  # REMIND Ensure all args are strings for join
    args_str = sep.join(args) + end
    # stdout_write(f'56:{file}')
    if file == sys.stderr:
        stderr_write(args_str)  # Keep original red error output for stderr.
    elif file in [sys.stdout, None]:
        # Get the caller's file and line number
        fra = sys._getframe(sys_getframe_n)
        line = fra.f_lineno
        file_name = fra.f_code.co_filename
        fun = fra.f_code.co_name
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        msg = f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}"  - {fun} - {args_str}'
        stdout_write(msg)
    else:  # For file objects like StringIO (used by traceback.print_exception), redirect content to preserve exception stack traces.
        print_raw(args_str, sep=sep, end=end, file=file)


def sprint(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2, only_print_on_main_process=False):
    if only_print_on_main_process:
        if multiprocessing.process.current_process().name == 'MainProcess':
            _sprint(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)
    else:
        _sprint(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=sys_getframe_n)


if __name__ == '__main__':
    str1 = 'O(^_^)O hello' * 40
    t1 = time.time()
    for i in range(10000):
        sprint(str1)

    print(time.time() - t1)
