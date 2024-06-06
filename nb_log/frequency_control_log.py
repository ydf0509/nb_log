import copy
import logging
import sys
import time
import typing

from nb_libs.sys_frame_uitils import EasyFrame


class FrequencyControlLog:
    file_line__ts_map = dict()

    def __init__(self, logger: logging.Logger, interval=10):
        self.logger = logger
        self.interval = interval

    @staticmethod
    def _pass(*args, **kwargs):
        pass

    def _fq(self, method):
        ef = EasyFrame(2)
        file_line = (ef.filename, ef.lineno)
        last_ts_log = self.file_line__ts_map.get(file_line, 0)
        if not self.interval:
            return method
        if time.time() - last_ts_log > self.interval:
            self.file_line__ts_map[file_line] = time.time()
            return method
        return self._pass

    @property
    def log(self, ) -> logging.Logger.log:
        return self._fq(self.logger.log)

    @property
    def debug(self, ) -> typing.Callable:
        return self._fq(self.logger.debug)

    @property
    def info(self, ) -> logging.Logger.info:
        return self._fq(self.logger.info)

    @property
    def warning(self, ) -> logging.Logger.warning:
        return self._fq(self.logger.warning)

    @property
    def error(self, ) -> logging.Logger.error:
        return self._fq(self.logger.error)

    @property
    def critical(self, ) -> logging.Logger.critical:
        return self._fq(self.logger.critical)

    # stacklevel 只能支持python3.9 以上的logging
    # def log(self, level, msg, *args, stacklevel=2, interval: int = None, **kwargs):
    #     ef = EasyFrame(1)
    #     file_line = (ef.filename, ef.lineno)
    #     last_ts_log = self.file_line__ts_map.get(file_line, 0)
    #     if not interval:
    #         self.logger.log(level, msg, *args, stacklevel=stacklevel, **kwargs)
    #     else:
    #         if time.time() - last_ts_log > interval:
    #             self.logger.log(level, msg, *args, stacklevel=stacklevel, **kwargs)
    #             self.file_line__ts_map[file_line] = time.time()
