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

FQ_CAPTURE_WARNINGS_LOGGER_NAME = 'fq_capture_warnings'  # Frequency-controlled warning logger


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
            file_line__ts[key] = time.time()
            s = warnings.formatwarning(message, category, filename, lineno, line)
            GlobalVars.logger.warning("%s", s)



def capture_warnings_with_frequency_control(capture: bool = True, interval=10):
    """
    Rate-limit warnings from the same file/line to prevent log flooding.
    """
    warnings.simplefilter('always', )  # Always show warnings to prevent __warningregistry__ memory leaks, then use frequency-controlled logging.
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
