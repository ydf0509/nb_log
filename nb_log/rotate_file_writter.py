import atexit
import multiprocessing
import queue
import threading
from pathlib import Path
import time


# from simple_print import sprint

def build_current_date_str():
    return time.strftime('%Y-%m-%d')


class FileWritter:
    _lock = threading.Lock()
    need_write_2_file = True

    def __init__(self, file_name: str, log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000, back_count=10):
        self._max_bytes = max_bytes
        self._back_count = back_count
        if self.need_write_2_file:
            self._file_name = file_name
            self.log_path = log_path
            if not Path(self.log_path).exists():
                print(f'自动创建日志文件夹 {log_path}')
                Path(self.log_path).mkdir(exist_ok=True)
            self._open_file()
            self._last_write_ts = 0
            self._last_del_old_files_ts = 0

    @property
    def file_path(self):
        f_list = []
        for f in Path(self.log_path).glob(f'????-??-??.????.{self._file_name}'):
            f_list.append(f)
        sn_list = []
        for f in f_list:
            if f'{build_current_date_str()}.' in f.name:
                sn = f.name.split('.')[1]
                sn_list.append(sn)
        if not sn_list:
            return Path(self.log_path) / Path(f'{build_current_date_str()}.0001.{self._file_name}')
        else:
            sn_max = max(sn_list)
            if (Path(self.log_path) / Path(f'{build_current_date_str()}.{sn_max}.{self._file_name}')).stat().st_size > self._max_bytes:
                new_sn_int = int(sn_max) + 1
                new_sn_str = str(new_sn_int).zfill(4)
                return Path(self.log_path) / Path(f'{build_current_date_str()}.{new_sn_str}.{self._file_name}')
            else:
                return Path(self.log_path) / Path(f'{build_current_date_str()}.{sn_max}.{self._file_name}')

    def _open_file(self):
        self._f = open(self.file_path, encoding='utf8', mode='a')

    def _close_file(self):
        self._f.close()

    def write_2_file(self, msg):
        if self.need_write_2_file:
            with self._lock:
                now_ts = time.time()
                if now_ts - self._last_write_ts > 10:
                    self._last_write_ts = time.time()
                    self._close_file()
                    self._open_file()
                self._f.write(msg)
                self._f.flush()
                if now_ts - self._last_del_old_files_ts > 30:
                    self._last_del_old_files_ts = time.time()
                    self._delete_old_files()

    def _delete_old_files(self):
        f_list = []
        for f in Path(self.log_path).glob(f'????-??-??.????.{self._file_name}'):
            f_list.append(f)
        # f_list.sort(key=lambda f:f.stat().st_mtime,reverse=True)
        f_list.sort(key=lambda f: f.name, reverse=True)
        for f in f_list[self._back_count:]:
            try:
                print(f'删除 {f}')
                f.unlink()
            except FileNotFoundError:
                pass

        # for i in range(10, 100):
        #     file_path = Path(self.log_path) / Path(DatetimeConverter(time.time() - 86400 * i).date_str + '.' + self._file_name)
        #     try:
        #         file_path.unlink()
        #     except FileNotFoundError:
        #         pass


# class PrintFileWritter(FileWritter):
#     _lock = threading.Lock()
#     need_write_2_file = False if nb_log_config_default.PRINT_WRTIE_FILE_NAME in (None, '') else True
#
#
# class StdFileWritter(FileWritter):
#     _lock = threading.Lock()
#     need_write_2_file = False if nb_log_config_default.SYS_STD_FILE_NAME in (None, '') else True


class BulkFileWritter:
    _lock = threading.Lock()
    need_write_2_file = True

    filename__queue_map = {}
    filename__options_map = {}
    filename__file_writter_map = {}

    _get_queue_lock = threading.Lock()

    _has_start_bulk_write = False

    @classmethod
    def _get_queue(cls, file_name):
        with cls._get_queue_lock:
            if file_name not in cls.filename__queue_map:
                cls.filename__queue_map[file_name] = queue.SimpleQueue()
            return cls.filename__queue_map[file_name]

    @classmethod
    def _get_file_writter(cls, file_name):
        if file_name not in cls.filename__file_writter_map:
            fw = FileWritter(**cls.filename__options_map[file_name])
            cls.filename__file_writter_map[file_name] = fw
        return cls.filename__file_writter_map[file_name]

    def __init__(self, file_name: str, log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000, back_count=10):
        self._file_name = file_name
        if file_name:
            self.__class__.filename__options_map[file_name] = {
                'file_name': file_name,
                'log_path': log_path,
                'max_bytes': max_bytes,
                'back_count': back_count,
            }
            self.start_bulk_write()

    def write_2_file(self, msg):
        if self.need_write_2_file:
            with self._lock:
                self._get_queue(self._file_name).put(msg)

    @classmethod
    def _bulk_real_write(cls):
        with cls._lock:
            for _file_name, queue in cls.filename__queue_map.items():
                msg_str_all = ''
                while not queue.empty():
                    msg_str_all += queue.get()
                if msg_str_all:
                    cls._get_file_writter(_file_name).write_2_file(msg_str_all)

    @classmethod
    def _when_exit(cls):
        print('结束')
        return cls._bulk_real_write()

    @classmethod
    def start_bulk_write(cls):
        def _bulk_write():
            while 1:
                cls._bulk_real_write()
                time.sleep(0.1)

        if not cls._has_start_bulk_write:
            cls._has_start_bulk_write = True
            threading.Thread(target=_bulk_write, daemon=True).start()


atexit.register(BulkFileWritter._when_exit)


def tt():
    fw = FileWritter('test_file6.log', '/test_dir2', max_bytes=1000 * 1000 * 10)
    t1 = time.time()
    for i in range(10000):
        # time.sleep(0.001)
        msg = f'yyy{str(i).zfill(5)}' * 40
        print(msg)
        fw.write_2_file(msg + '\n')
    print(time.time() - t1)


if __name__ == '__main__':
    multiprocessing.Process(target=tt).start()
    multiprocessing.Process(target=tt).start()
    # tt()
