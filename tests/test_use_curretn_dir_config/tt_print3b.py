import atexit
import os

import queue
import sys
import threading
import time
from pathlib import Path
import multiprocessing
from chained_mode_time_tool import DatetimeConverter


class FileWritter:
    _lock = threading.Lock()
    need_write_2_file = True

    def __init__(self, file_name: str, log_path='/pythonlogs'):
        if self.need_write_2_file:
            print(f'shilihua  {multiprocessing.current_process().pid}')
            self._file_name = file_name
            self.log_path = log_path
            if not Path(self.log_path).exists():
                # sprint(f'自动创建日志文件夹 {log_path}')
                Path(self.log_path).mkdir(exist_ok=True)
            self._open_file()
            self._last_write_ts = time.time()
            self._last_del_old_files_ts = time.time()

    def _open_file(self):
        self.file_path = Path(self.log_path) / Path(DatetimeConverter().date_str + '.' + self._file_name)
        self._f = open(self.file_path, encoding='utf8', mode='a')

    def _close_file(self):
        self._f.close()

    def write_2_file(self, msg):
        if self.need_write_2_file:
            with self._lock:
                now_ts = time.time()
                if now_ts - self._last_write_ts > 5:
                    self._last_write_ts = time.time()
                    self._close_file()
                    self._open_file()
                self._f.write(msg)
                self._f.flush()
                if now_ts - self._last_del_old_files_ts > 300:
                    self._last_del_old_files_ts = time.time()
                    self._delete_old_files()

    def _delete_old_files(self):
        for i in range(10, 100):
            file_path = Path(self.log_path) / Path(DatetimeConverter(time.time() - 86400 * i).date_str + '.' + self._file_name)
            try:
                file_path.unlink()
            except FileNotFoundError:
                pass

    def start_bulk_write(self):
        pass



class NyDaemonThread(threading.Thread):
    def _stop(self):
        lock = self._tstate_lock
        if lock is not None:
            assert not lock.locked()
        self._is_stopped = True
        self._tstate_lock = None
        if not self.daemon:
            print(1067, 'yyyy')
            with threading._shutdown_locks_lock:
                # Remove our lock and other released locks from _shutdown_locks
                threading._maintain_shutdown_locks()


class BulkFileWrite(FileWritter):

    q =queue.SimpleQueue()

    def __init__(self, file_name: str, log_path='/pythonlogs'):
        super().__init__(file_name,log_path)
        atexit.register(self._at_exit)


    def write_2_file(self, msg):
        if self.need_write_2_file:
            with self._lock:
                self.q.put(msg)


    def _bulk_write(self):
        while 1:
            self._bulk_write0()
            time.sleep(0.1)

    def _at_exit(self):
        pid = multiprocessing.current_process().name
        print(f'要退出 {pid}')
        self._bulk_write0()

    def _bulk_write0(self):
        with self._lock:
            msg_list = []
            while 1:
                if not self.q.empty():
                    msg_list.append(self.q.get())
                else:
                    break
            if msg_list:
                self._close_file()
                self._open_file()
                self._f.write('\n'.join(msg_list))
                self._f.flush()



    def start_bulk_write(self):
        NyDaemonThread(target=self._bulk_write,daemon=True).start()




print_raw = print
WORD_COLOR = 37


def stdout_write(msg: str):
    sys.stdout.write(msg)
    sys.stdout.flush()


def stderr_write(msg: str):
    sys.stderr.write(msg)
    sys.stderr.flush()

# print_file_writter = FileWritter('xx3.test')
print_file_writter = BulkFileWrite('xx3.test')
print_file_writter.start_bulk_write()
print_file_writter.need_write_2_file=True
print(print_file_writter.need_write_2_file)
def _print_with_file_line(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2):
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
        now = None
        for i in range(1):
            now = time.strftime("%H:%M:%S")

        # line = None
        # file_name = None
        # fun =None
        # now = None

        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        1 + 2
        stdout_write(
            f'{now}  "{file_name}:{line}"  {fun} {args_str} ')
        # print_file_writter.write_2_file(f'{now}  "{file_name}:{line}" {fun} {args_str} ')

    else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
        pass


# noinspection PyProtectedMember,PyUnusedLocal,PyIncorrectDocstring,DuplicatedCode
def nb_print(*args, sep=' ', end='\n', file=None, flush=True):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    _print_with_file_line(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)

def tt1():
    pid = multiprocessing.current_process().name
    t1 = time.time()
    def f():
        # import nb_log

        for i in range(10000):
            msg = f'{pid} {i} hh'
            # nb_print(msg*1)
            print_file_writter.write_2_file(msg*1)

    f()


    print(time.time() -t1)

def tt2():
    import logging
    logger = logging.getLogger('abcd')

    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - "%(filename)s %(lineno)d -" ', "%Y-%m-%d %H:%M:%S")

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    fh = logging.FileHandler('testlog3.log')
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    t1 = time.time()
    for i in range(10000):
        logger.error(f'xxxxxx{i}'*20)
    print(time.time() - t1)

if __name__ == '__main__':
    # from auto_run_on_remote import run_current_script_on_remote
    # run_current_script_on_remote()
    # print(osx.getgid())
    # tt1()
    multiprocessing.Process(target=tt1).start()
    multiprocessing.Process(target=tt1).start()
