import logging
import time
import warnings
from collections import defaultdict
import nb_log

_warnings_showwarning = None


class GlobalVars:
    interval = None
    logger = None


file_line__ts = defaultdict(float)

FQ_CAPTURE_WARNINGS_LOGGER_NAME = 'fq_capture_warnings'  # 控频日志


def _frequency_control_showwarning(message, category, filename, lineno, file=None, line=None):
    """
    Implementation of showwarnings which redirects to logging, which will first
    check to see if the file parameter is None. If a file is specified, it will
    delegate to the original warnings implementation of showwarning. Otherwise,
    it will call warnings.formatwarning and will log the resulting string to a
    warnings logger named "py.warnings" with level logging.WARNING.
    """
    if file is not None:
        if _warnings_showwarning is not None:
            _warnings_showwarning(message, category, filename, lineno, file, line)
    else:
        key = (filename, lineno)
        last_show_log_ts = file_line__ts[key]
        if time.time() - last_show_log_ts > GlobalVars.interval:
            s = warnings.formatwarning(message, category, filename, lineno, line)
            GlobalVars.logger.warning("%s", s)
            file_line__ts[key] = time.time()


def capture_warnings_with_frequency_control(capture: bool = True, interval=10):
    """
    对相同文件代码行的警告,使用控频来记录警告
    """
    warnings.simplefilter('always', )  # 先设置成始终打印警告,防止python维护 __warningregistry__ 字典造成内存泄漏,然后使用上面的控频日志来记录.
    global _warnings_showwarning
    GlobalVars.logger = nb_log.get_logger(FQ_CAPTURE_WARNINGS_LOGGER_NAME, log_filename=f'{FQ_CAPTURE_WARNINGS_LOGGER_NAME}.log')
    if capture:
        if _warnings_showwarning is None:
            _warnings_showwarning = warnings.showwarning
            warnings.showwarning = _frequency_control_showwarning
    else:
        if _warnings_showwarning is not None:
            warnings.showwarning = _warnings_showwarning
            _warnings_showwarning = None
    GlobalVars.interval = interval
