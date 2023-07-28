import atexit
import os
import sys
import re
import queue
import threading
import time
# from nb_log.file_write import StdFileWritter
from nb_log.rotate_file_writter import OsFileWritter
from nb_log import nb_log_config_default

stdout_raw = sys.stdout.write
stderr_raw = sys.stderr.write

dele_color_pattern = re.compile('\\033\[.+?m')

sys_std_file_name = os.environ.get('SYS_STD_FILE_NAME', None) or nb_log_config_default.SYS_STD_FILE_NAME
std_writter = OsFileWritter(sys_std_file_name,log_path=nb_log_config_default.LOG_PATH,
                            back_count=nb_log_config_default.LOG_FILE_BACKUP_COUNT,max_bytes=nb_log_config_default.LOG_FILE_SIZE * 1024 * 1024)

is_win = True if os.name == 'nt' else False



class BulkStdout:
    q = queue.SimpleQueue()
    _lock = threading.Lock()
    _has_start_bulk_stdout = False

    @classmethod
    def _bulk_real_stdout(cls):
        with cls._lock:
            msg_str_all = ''
            while not cls.q.empty():
                msg_str_all += cls.q.get()
            if msg_str_all:
                stdout_raw(msg_str_all)

    @classmethod
    def stdout(cls, msg):
        with cls._lock:
            cls.q.put(msg)

    @classmethod
    def _when_exit(cls):
        # stdout_raw('结束 stdout_raw')
        return cls._bulk_real_stdout()

    @classmethod
    def start_bulk_stdout(cls):
        def _bulk_stdout():
            while 1:
                cls._bulk_real_stdout()
                time.sleep(0.05)

        if not cls._has_start_bulk_stdout:
            cls._has_start_bulk_write = True
            threading.Thread(target=_bulk_stdout, daemon=True).start()


if is_win and nb_log_config_default.USE_BULK_STDOUT_ON_WINDOWS:
    BulkStdout.start_bulk_stdout()
    atexit.register(BulkStdout._when_exit)


def monkey_sys_stdout(msg):
    if is_win and nb_log_config_default.USE_BULK_STDOUT_ON_WINDOWS:
        BulkStdout.stdout(msg)
    else:
        stdout_raw(msg)
    msg_delete_color = dele_color_pattern.sub('', msg)
    std_writter.write_2_file(msg_delete_color)
    # std_writter.write_2_file(msg)


def monkey_sys_stderr(msg):
    stderr_raw(msg)
    msg_delete_color = dele_color_pattern.sub('', msg)
    std_writter.write_2_file(msg_delete_color)


def patch_sys_std():
    sys.stdout.write = monkey_sys_stdout
    sys.stderr.write = monkey_sys_stderr
