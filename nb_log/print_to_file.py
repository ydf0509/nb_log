import threading
from pathlib import Path
from nb_log import nb_log_config_default
import time

need_write_2_file = False if nb_log_config_default.PRINT_WRTIE_FILE_NAME in (None, '') else True


class Print2File:
    lock = threading.Lock()

    def __init__(self):
        if need_write_2_file:
            self._open_file()
            self._last_write_ts = time.time()

    def _open_file(self):
        self.print_file_path = Path(nb_log_config_default.LOG_PATH) / (time.strftime('%Y-%m-%d',time.localtime()) + '.' + nb_log_config_default.PRINT_WRTIE_FILE_NAME)
        self._f = open(self.print_file_path, encoding='utf8', mode='a')

    def _close_file(self):
        self._f.close()

    def write_2_file(self, msg):
        if need_write_2_file:
            with self.lock:
                if time.time() - self._last_write_ts > 5:
                    self._close_file()
                    self._open_file()
                    self._last_write_ts = time.time()
                self._f.write(msg + '\n')
                self._f.flush()


if __name__ == '__main__':
    Print2File().write_2_file('哈哈哈')
