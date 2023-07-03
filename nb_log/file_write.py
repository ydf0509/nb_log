import threading
from functools import wraps
from pathlib import Path
from nb_log import nb_log_config_default
import time
from chained_mode_time_tool import DatetimeConverter
from nb_log.simple_print import sprint


def singleton(cls):
    """
    单例模式装饰器,新加入线程锁，更牢固的单例模式，主要解决多线程如100线程同时实例化情况下可能会出现三例四例的情况,实测。
    """
    _instance = {}
    singleton.__lock = threading.Lock()  # 这里直接演示了线程安全版单例模式

    @wraps(cls)
    def _singleton(*args, **kwargs):
        with singleton.__lock:
            if cls not in _instance:
                _instance[cls] = cls(*args, **kwargs)
            return _instance[cls]

    return _singleton


# @singleton
class FileWritter:
    _lock = threading.Lock()
    need_write_2_file = True

    def __init__(self, file_name: str, log_path=nb_log_config_default.LOG_PATH):
        if self.need_write_2_file:
            self._file_name = file_name
            self.log_path = log_path
            if not Path(self.log_path).exists():
                sprint(f'自动创建日志文件夹 {log_path}')
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


class PrintFileWritter(FileWritter):
    _lock = threading.Lock()
    need_write_2_file = False if nb_log_config_default.PRINT_WRTIE_FILE_NAME in (None, '') else True


class StdFileWritter(FileWritter):
    _lock = threading.Lock()
    need_write_2_file = False if nb_log_config_default.SYS_STD_FILE_NAME in (None, '') else True


if __name__ == '__main__':
    FileWritter('test_file', '/test_dir2').write_2_file('哈哈哈')
