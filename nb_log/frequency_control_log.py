import copy
import logging
import sys
import time

from nb_libs.sys_frame_uitils import EasyFrame


class FrequencyControlLog:
    file_line__ts_map = dict()

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log(self, level, msg, *args, stacklevel=2, interval: int = None, **kwargs):
        ef = EasyFrame(1)
        file_line = (ef.filename, ef.lineno)
        last_ts_log = self.file_line__ts_map.get(file_line, 0)
        if not interval:
            self.logger.log(level, msg, *args, stacklevel=stacklevel, **kwargs)
        else:
            if time.time() - last_ts_log > interval:
                self.logger.log(level, msg, *args, stacklevel=stacklevel, **kwargs)
                self.file_line__ts_map[file_line] = time.time()
