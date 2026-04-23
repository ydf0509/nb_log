# coding=utf8
"""
This file nb_log_config.py is auto-generated into the root directory of the Python project (at sys.path[1]).
Variables defined here will override the values in nb_log_config_default. This serves as the default configuration for nb_log.
Users do not need to modify the config file inside the nb_log package installation directory.

The final configuration is determined by the parameters passed to get_logger_and_add_handlers().
If a parameter is None, the value defined here will be used.
"""

"""
To disable colored log output, set DEFAULUT_USE_COLOR_HANDLER = False
To disable block background colors in console, set DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
To suppress the PyCharm color settings hint, set WARNING_PYCHARM_COLOR_SETINGS = False
To change the log format template, set FORMATTER_KIND (7 built-in templates available, or add custom ones)
LOG_PATH sets the directory for log file storage.
"""
import sys
# noinspection PyUnresolvedReferences
import logging
import os
# noinspection PyUnresolvedReferences
from pathlib import Path  # noqa
import socket
from pythonjsonlogger.jsonlogger import JsonFormatter

def judge_has_set_pythonpath() -> bool:
    """
    Judge whether PYTHONPATH is set.
    :return:
    """
    try:
        sys_path1_parent2 = Path(sys.path[1]).parents[2]
        if sys_path1_parent2 == Path(sys.executable).parents[2]:
            return False
        else:
            return True
    except IndexError:
        return True

def aut_get_proj_name() -> str:
    """
    Automatically determine the project name from the sys.path[1] directory.
    :return:
    """
    if judge_has_set_pythonpath() is False:
        """
         # For example /home/ydfwsl/miniconda3/lib/python37.zip, this usually happens because PYTHONPATH is not set to the project root directory.
         1. PyCharm IDE automatically adds the opened project root directory to PYTHONPATH.

         2. In VSCode, users should set the following in settings.json:
              {
                "python.analysis.extraPaths": ["${workspaceFolder}"],
                "terminal.integrated.env.windows": { "PYTHONPATH": "${workspaceFolder};${env:PYTHONPATH}" },
                "terminal.integrated.env.osx": { "PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}" },
                "terminal.integrated.env.linux": { "PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}" }
              }

         3. If manually starting Python scripts in cmd, PowerShell, or Linux, you need to manually set PYTHONPATH to the project root directory.
            Simply cd into the project root directory first, then execute the corresponding command:
            CMD: set PYTHONPATH=%cd%
            PowerShell: $env:PYTHONPATH = $PWD.Path
            Linux/macOS: export PYTHONPATH=$PWD

        """
        return 'no_proj_name'
    else:
        return Path(sys.path[1]).name 

# PRINT_WRTIE_FILE_NAME is an advanced feature unique to nb_log, beyond the scope of typical logging packages.
# Controls whether print output is automatically written to a file. Set to None to disable. A new file is created daily (e.g. 2023-06-30.my_proj.print) in LOG_PATH.
# If you set the environment variable PRINT_WRTIE_FILE_NAME (e.g. export PRINT_WRTIE_FILE_NAME="my_proj.print"), it takes priority over the value in nb_log_config.py.
PRINT_WRTIE_FILE_NAME = os.environ.get("PRINT_WRTIE_FILE_NAME") or aut_get_proj_name() + '.print'

# SYS_STD_FILE_NAME is an advanced feature unique to nb_log, beyond the scope of typical logging packages.
# All stdout output (including print and StreamHandler logs) is written to this file. Set to None to disable. A new file is created daily (e.g. 2023-06-30.my_proj.std) in LOG_PATH.
# If you set the environment variable SYS_STD_FILE_NAME (e.g. export SYS_STD_FILE_NAME="my_proj.std"), it takes priority over the value in nb_log_config.py.
# This is similar to nohup redirecting all screen output to a nohup.out file - a unique feature of nb_log that logging and loguru don't offer.
# While different logger namespaces may write to dozens of separate log files, SYS_STD_FILE_NAME consolidates all project logs into a single file.
SYS_STD_FILE_NAME = os.environ.get("SYS_STD_FILE_NAME") or aut_get_proj_name() + '.std'

USE_BULK_STDOUT_ON_WINDOWS = False  # Whether to batch stdout every 0.1s on Windows (Windows I/O performance is poor)

DEFAULUT_USE_COLOR_HANDLER = True  # Whether to use colored log output by default.
DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = False  # Whether to use loguru's console handler instead of nb_log's ColorHandler by default.
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True  # Whether to display block background colors in console logs. Set to False to disable background colors.
AUTO_PATCH_PRINT = True  # Whether to auto-patch print with monkey patch. When patched, print output is colorized and clickable for navigation.

# The following settings control startup hints in the console. Before disabling them, make sure you understand what each hint is for.
SHOW_PYCHARM_COLOR_SETINGS = True  # Set to False to suppress the PyCharm console color optimization hint at startup.
SHOW_NB_LOG_LOGO = True  # Set to False to suppress the nb_log ASCII logo at startup.
SHOW_IMPORT_NB_LOG_CONFIG_PATH = True  # Whether to print the path of the loaded nb_log_config.py file. See https://github.com/ydf0509/pythonpathdemo for PYTHONPATH details.

WHITE_COLOR_CODE = 37  # Different PyCharm versions/themes use different codes for white (37 or 97). Adjust based on your PyCharm console color settings.

DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER = False  # Whether to automatically write logs to a file even when log_filename is not specified (auto-generates namespace.log).
AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = False  # Automatically write ERROR level and above to a separate file, with filename auto-generated from log_filename.
LOG_FILE_SIZE = 1000  # Max size per log file in MB. Files are rotated when this size is exceeded.
LOG_FILE_BACKUP_COUNT = 10  # Max number of backup files to keep per log file. Older backups are deleted.

LOG_PATH = os.getenv("LOG_PATH")  # Priority: read from environment variable first (e.g. export LOG_PATH='/your/log/dir/')
if not LOG_PATH:
    LOG_PATH = '/pythonlogs'  # Default log directory, located at the root of the drive where the project resides.
    # LOG_PATH = Path(__file__).absolute().parent / Path("pythonlogs")   # This would create a pythonlogs folder in the project root.
    if os.name == 'posix':  # Non-root Linux/Mac users don't have write access to /pythonlogs, so default to ~/pythonlogs instead.
        home_path = os.environ.get("HOME", '/')  # Gets the current user's home directory on Linux/Mac
        LOG_PATH = Path(home_path) / Path('pythonlogs')  # Linux/Mac permissions are strict; non-root users can't write to /pythonlogs.
# print('LOG_PATH:',LOG_PATH)

LOG_FILE_HANDLER_TYPE = 6  # 1 2 3 4 5 6 7   # nb_log file rotation - all options are multi-process safe.
"""
LOG_FILE_HANDLER_TYPE can be set to one of the following values:
1 - Multi-process safe size-based rotation with batch writing to reduce file lock operations.
    In tests with 10 processes, performance is 100x better than type 5 on Windows, 5x better on Linux.
2 - Multi-process safe daily rotation. A new log file is created each day with a date suffix.
3 - Single file without rotation (no rotation means no multi-process safety concerns).
4 - WatchedFileHandler (Linux only). Relies on external logrotate for file rotation. Multi-process safe.
5 - Third-party concurrent_log_handler.ConcurrentRotatingFileHandler for size-based rotation.
    Uses file locks (fcntl on Linux, win32con on Windows). Performance on Windows is very poor.
    For size-based rotation, type 1 is recommended over type 5.
6 - BothDayAndSizeRotatingFileHandler. Custom implementation that rotates by both time and size.
    Files are rotated whenever either the size or time threshold is reached.
7 - LoguruFileHandler. Uses the well-known loguru package's file handler for writing logs.
"""

LOG_LEVEL_FILTER = logging.DEBUG  # Default log level when not specified in get_logger(). Logs below this level are ignored (e.g. if set to INFO, debug logs are suppressed).
# It is strongly discouraged to raise this globally to INFO. Use logger namespaces to adjust levels for verbose loggers individually.
# See https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c9.html#id2 for details on logger namespace usage.

ROOT_LOGGER_LEVEL = logging.INFO  # Log level for the root logger namespace. If INFO, all unhandled loggers will capture INFO and above.
ROOT_LOGGER_FILENAME = 'root.log'  # Filename for root logger logs. Set to None to disable file logging for root.
ROOT_LOGGER_FILENAME_ERROR = 'root.error.log'  # Separate filename for ERROR level and above from root logger. Set to None to disable.

# Filter console output by keywords. If a message contains any string in this list, it will be suppressed.
# This applies to both print and logger console output. Useful for filtering verbose prints from third-party packages.
# Avoid adding too many entries as it may slightly affect performance.
FILTER_WORDS_PRINT = []  # e.g. FILTER_WORDS_PRINT = ['noisy_module', 'verbose_warning'] to suppress messages containing these strings.


def get_host_ip():
    ip = ''
    host_name = ''
    # noinspection PyBroadException
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sc.connect(('8.8.8.8', 80))
        ip = sc.getsockname()[0]
        host_name = socket.gethostname()
        sc.close()
    except Exception:
        pass
    return ip, host_name


computer_ip, computer_name = get_host_ip()


class JsonFormatterJumpAble(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        # log_record['jump_click']   = f"""File '{record.__dict__.get('pathname')}', line {record.__dict__.get('lineno')}"""
        log_record[f"{record.__dict__.get('pathname')}:{record.__dict__.get('lineno')}"] = ''  # Add a clickable jump-to-source field.
        log_record['ip'] = computer_ip
        log_record['host_name'] = computer_name
        super().add_fields(log_record, record, message_dict)
        if 'for_segmentation_color' in log_record:
            del log_record['for_segmentation_color']


DING_TALK_TOKEN = '3dd0eexxxxxadab014bd604XXXXXXXXXXXX'  # DingTalk alert bot token

EMAIL_HOST = ('smtp.sohu.com', 465)
EMAIL_FROMADDR = 'aaa0509@sohu.com'  # 'matafyhotel-techl@matafy.com',
EMAIL_TOADDRS = ('cccc.cheng@silknets.com', 'yan@dingtalk.com',)
EMAIL_CREDENTIALS = ('aaa0509@sohu.com', 'abcdefg')

ELASTIC_HOST = '127.0.0.1'
ELASTIC_PORT = 9200

KAFKA_BOOTSTRAP_SERVERS = ['192.168.199.202:9092']
ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT = False

MONGO_URL = 'mongodb://myUserAdmin:mimamiama@127.0.0.1:27016/admin'

RUN_ENV = 'test'

FORMATTER_DICT = {
    1: logging.Formatter(
        'Time[%(asctime)s] - Logger[%(name)s] - File[%(filename)s] - Line[%(lineno)d] - Level[%(levelname)s] - Message[%(message)s]',
        "%Y-%m-%d %H:%M:%S"),
    2: logging.Formatter(
        '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),
    3: logging.Formatter(
        '%(asctime)s - %(name)s - [ File "%(pathname)s", line %(lineno)d, in %(funcName)s ] - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # Traceback-style template with clickable file path
    4: logging.Formatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
        "%Y-%m-%d %H:%M:%S"),  # Also supports clickable log navigation
    5: logging.Formatter(
        '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # Recommended template
    6: logging.Formatter('%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
                         "%Y-%m-%d %H:%M:%S"),
    7: logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # Short filename with line number

    8: JsonFormatterJumpAble('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s %(lineno)d  %(process)d %(thread)d', "%Y-%m-%d %H:%M:%S.%f",
                             json_ensure_ascii=False),  # JSON format, ideal for ELK stack ingestion and analysis.

    9: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # Enhanced template 5 with process and thread info.
    10: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # Enhanced template 7 with process and thread info.
    11: logging.Formatter(
        f'%(asctime)s-({computer_ip},{computer_name})-[p%(process)d_t%(thread)d] - %(name)s - "%(filename)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # Enhanced template 7 with process, thread, IP, and hostname.
}

FORMATTER_KIND = 5  # Default formatter template index when not specified in get_logger()
