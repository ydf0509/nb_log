
# 1. Introduction to nb_log

**[中文 README / Chinese Documentation](https://github.com/ydf0509/nb_log/blob/master/README.md)**

[nb_log readthedocs documentation](https://nb-log-doc.readthedocs.io/zh_CN/latest)

[nb_log source code](https://github.com/ydf0509/nb_log)

[//]: # ([![image.png]&#40;https://i.postimg.cc/ydqgWDRW/image.png&#41;]&#40;https://postimg.cc/HJ2shsBC&#41;)

[![pkFSfc8.png](https://s21.ax1x.com/2024/04/29/pkFSfc8.png)](https://imgse.com/i/pkFSfc8)



This document is quite long, but most of it is not about nb_log usage — it reviews the concepts of Python's built-in `logging` module.
Many Python developers don't understand the `logging` namespace concept, the tree-structured namespace hierarchy, or the relationship between handlers and loggers, which is why such detailed explanation is necessary.

Many Pythonistas still don't know what the first parameter of `logging.getLogger()` does, which leads to confusion about how to use multiple namespaces in nb_log.

## Tips: For even simpler logging, install kuai_log

pip install kuai_log

```
kuai_log is NOT built on top of logging, but it is 100% API-compatible with
the logging module's method names and parameters.
Every method and parameter in kuai_log's KuaiLogger also exists in logging.Logger,
but some niche methods from logging may not be present in kuai_log.

kuai_log is 30x faster than logging and loguru, and 4x faster than nb_log.

kuai_log requires no config files — everything is controlled via function parameters.

kuai_log has zero third-party dependencies, whereas nb_log depends on some third-party packages.
```

## nb_log vs logging vs loguru — Quick Comparison

| Dimension              | loguru              | logging               | nb\_log                                    |
| ---------------------- | ------------------- | --------------------- | ------------------------------------------ |
| Ease of use            | ✅ Simple            | ❌ Verbose             | ✅ Simple                                   |
| Namespaces             | ❌ None              | ✅ Full support        | ✅ Full support                              |
| 3rd-party compatibility| ❌ Easily pollutes   | ✅ Safe                | ✅ Safe                                      |
| Pretty output          | ✅ Great by default  | ❌ Needs configuration | ✅ Beautiful by default                      |
| Extensibility          | ⚠️ Limited          | ✅ High                | ✅ Higher (multi-handler support)            |
| Getting started        | ✅ Quick & easy      | ❌ Tedious & complex   | ✅ Great logging in one second               |


## 1.0 Installing nb_log

pip install nb_log

## 1.0.1 nb_log is more than just logging — it also monkey-patches print and sys.stdout/sys.stderr

It monkey-patches the built-in `print` function, automatically displaying the filename and exact line number where `print` was called. No more hunting for stray `print` statements scattered across your codebase.

It also patches `print` and the `sys.stdout`/`sys.stderr` used by `StreamHandler`, enabling all standard output to be automatically written to daily rotating files.
(See the `SYS_STD_FILE_NAME` and `PRINT_WRTIE_FILE_NAME` settings in section 1.1.d.)


## 1.0.2 nb_log now supports loguru-style logging — native loguru for console and file output (see section 1.10.b)

With this feature, there's really no reason to say nb_log is inferior to loguru — loguru is essentially a subset of nb_log.

loguru console output screenshot:
[![pkFShjS.png](https://s21.ax1x.com/2024/04/29/pkFShjS.png)](https://imgse.com/i/pkFShjS)

## 1.1 Basic nb_log Usage

Console logging:

```python
print('print before importing nb_log is plain')

from nb_log import get_logger

logger = get_logger('lalala',)   # Only the name parameter is required; all others are optional.
# logger = get_logger('lalala', log_filename='lalala.log', formatter_template=5, log_file_handler_type=2)  # get_logger has many optional params for customizing the logger.


logger.debug('debug is green — means debugging, code is OK')
logger.info('info is sky blue — normal log output')
logger.warning('yellow — a warning has occurred')
logger.error('magenta — an error in the code')
logger.critical('dark red — a critical error has occurred')

print('print after importing nb_log is enhanced with clickable jump links')
```

`nb_log` provides stunningly colorful log output, and even `print` gets automatic coloring — far more vibrant than `loguru`.
Traditional `logging` shows everything in a dull dark red regardless of level.
`loguru` differentiates levels slightly with different foreground colors on the level field.
`nb_log` uses **background + foreground color rendering** for each level and for print — the colors are unmissable. For example, `error` has a magenta background and `critical` has a dark red background.
**Even in a program producing tens of thousands of log lines per second, with nb_log, even someone with 800-degree myopia standing 10 meters from the screen can tell at a glance whether the program has errors.**


### 1.1.a Writing Logs to Files

By default, nb_log only prints to the console. It won't write logs to files, Kafka, MongoDB, Elasticsearch, email, or DingTalk unless you explicitly enable each destination with its own control parameter.

Only when `get_logger` is called with `log_filename` will that logger write to the specified file. The log file directory is configured via `LOG_PATH` in `nb_log_config.py`.

```python
from nb_log import get_logger
logger = get_logger('logger_namespace',
                    log_filename='namespace_file.log',
                    error_log_filename='f4b_error.log')
logger.debug('this log entry will be written to the file')
```

### 1.1.a2 Writing Logs to Files with Separate Error Log File

When `error_log_filename` is passed to `get_logger`, logs at ERROR level and above are also written to a separate error file.
Alternatively, you can set `AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = True` in `nb_log_config.py` to automatically write error-level logs to a separate file, with the filename auto-generated based on `log_filename`.

```python
from nb_log import get_logger
logger = get_logger('logger_namespace',
                    log_filename='namespace_file.log',
                    error_log_filename='namespace_file_error.log')
logger.debug('this log entry will be written to the normal log file')
logger.error('this log entry will be written to the normal file AND the error file')
```

### 1.1.b Core Parameters of get_logger

```doctest
   :param name: The logger namespace — this is the most important and most misunderstood parameter.
                Many Python developers still don't know what the first argument to logging.getLogger() does.
                The namespace is critically important: different names produce loggers with different behaviors.
                For example, you can configure the "aa" namespace to print to console AND write to file at INFO+ level,
                while the "bb" namespace only prints to console at DEBUG+ level.
                This is achieved through different logger namespaces.
        :param log_level_int: Log output level. Set to 1/2/3/4/5 corresponding to
               logging.DEBUG(10), logging.INFO(20), logging.WARNING(30), logging.ERROR(40), logging.CRITICAL(50).
               You can also directly use 10/20/30/40/50 (both are supported).
       :param is_add_stream_handler: Whether to print logs to the console.
       :param is_use_loguru_stream_handler: Whether to use loguru's console output.
              If None, uses the DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER value from nb_log_config.py.
       :param do_not_use_color_handler: Whether to disable colored log output.
       :param log_path: Directory path for storing log files. If not set, uses nb_log_config.LOG_PATH.
              If the config doesn't specify it either, a /pythonlogs folder is auto-created at the root of
              the disk where the code resides. On non-Windows systems, be aware of directory permissions.
       :param log_filename: Log filename. Logs are written to file only when BOTH log_path and log_filename are set.
       :param error_log_filename: Error log filename. If not None, error-level and above logs are
              also written to this separate file.
       :param log_file_size: Max log file size in MB. Default is 100MB.
       :param log_file_handler_type: Set to 1-7:
              1 = Multi-process safe, size-based rotating file handler (batch-write, reduced file lock operations;
                  100x faster on Windows and 5x faster on Linux compared to option 5)
              2 = Multi-process safe, daily rotating file handler (same file, new log file each day)
              3 = Non-rotating single file handler (no rotation = no multi-process safety concerns)
              4 = WatchedFileHandler (Linux only, requires external logrotate for file rotation, multi-process safe)
              5 = Third-party concurrent_log_handler.ConcurrentRotatingFileHandler (file-lock based,
                  multi-process safe rotation; fcntl on Linux is OK, but win32con on Windows is extremely slow.
                  For size-based rotation, use option 1 instead of 5.)
              6 = BothDayAndSizeRotatingFileHandler — a fully custom handler that rotates by both size AND time.
              7 = LoguruFileHandler — uses the loguru package's file handler for writing logs.
       :param mongo_url: MongoDB connection URL. If None, no MongoHandler is added.
       :param is_add_elastic_handler: Whether to log to Elasticsearch.
       :param is_add_kafka_handler: Whether to publish logs to Kafka.
       :param ding_talk_token: DingTalk robot token.
       :param ding_talk_time_interval: Minimum interval between DingTalk messages.
       :param mail_handler_config: Email handler configuration.
       :param is_add_mail_handler: Whether to send logs via email.
       :param formatter_template: Log format template. If an integer, it maps to the key in
                                nb_log_config.py's formatter_dict.
                                1 = verbose template, 2 = brief template, 5 = recommended template.
                                If a logging.Formatter object, it is used directly.
       :type log_level_int: int
       :type is_add_stream_handler: bool
       :type log_path: str
       :type log_filename: str
       :type mongo_url: str
       :type log_file_size: int
 
   
```

`log_filename` controls whether and where logs are written to file. Some people skip the docs and then ask why nb_log doesn't write log files.
Logger and Handler follow the Observer pattern — where logs get recorded depends entirely on which handlers have been added.

### 1.1.c Generating and Importing the nb_log Configuration File

When you first run any script that uses nb_log, it automatically creates an `nb_log_config.py` file in the `sys.path[1]` directory with default values. After that, nb_log automatically imports `nb_log_config`, and if successfully imported, a console message tells you which file was loaded as the configuration.

If running from the command line or on Linux (not in PyCharm), you need to set `PYTHONPATH` to your project root. This way, nb_log can auto-generate or locate `nb_log_config.py` in the project root.

You can run `print(sys.path)` and `print(sys.path[1])` to see what `sys.path[1]` resolves to.

If you're not sure what PYTHONPATH does, read this article:

[Introduction to PYTHONPATH](https://github.com/ydf0509/pythonpathdemo)


### 1.1.d Configuration Parameters in nb_log_config.py

Users can modify `nb_log_config.py` values as needed.

`nb_log_config.py`    
```python

# coding=utf8
"""
This file nb_log_config.py is auto-generated in the root of your Python project (at sys.path[1]).
Variables defined here override the defaults from nb_log_config_default.
Users should NOT modify the nb_log package's built-in config file.

The final configuration is determined by get_logger_and_add_handlers parameters — if a parameter is None,
the value from this config file is used.
"""

"""
To disable colored logging entirely, set DEFAULUT_USE_COLOR_HANDLER = False
To disable block-style background colors, set DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
To suppress nb_log's PyCharm color setup tips, set WARNING_PYCHARM_COLOR_SETINGS = False
To change the log format template, set the FORMATTER_KIND parameter (7 built-in templates, or add your own)
LOG_PATH sets the directory for log files.
"""
import sys
# noinspection PyUnresolvedReferences
import logging
import os
# noinspection PyUnresolvedReferences
from pathlib import Path  # noqa
import socket
from pythonjsonlogger.jsonlogger import JsonFormatter

# PRINT_WRTIE_FILE_NAME — an advanced feature far beyond ordinary logging packages; a unique nb_log capability.
# Whether to auto-write project print output to a file. Set to None to disable.
# Auto-generates one file per day, e.g. 2023-06-30.my_proj.print, in the LOG_PATH directory.
# If the PRINT_WRTIE_FILE_NAME environment variable is set, it takes priority over this config value.
PRINT_WRTIE_FILE_NAME = os.environ.get("PRINT_WRTIE_FILE_NAME") or Path(sys.path[1]).name + '.print'

# SYS_STD_FILE_NAME — another advanced nb_log exclusive feature.
# Captures ALL standard output (not just print, but also StreamHandler logs) to a file.
# Set to None to disable. Auto-generates one file per day, e.g. 2023-06-30.my_proj.std, in the LOG_PATH directory.
# If the SYS_STD_FILE_NAME environment variable is set, it takes priority over this config value.
# This is essentially the equivalent of nohup's output redirection — a capability unique to nb_log,
# not available in logging or loguru.
# While different logger namespaces may write to dozens of separate log files,
# SYS_STD_FILE_NAME consolidates all output into a single file.
SYS_STD_FILE_NAME = os.environ.get("SYS_STD_FILE_NAME") or Path(sys.path[1]).name + '.std'

USE_BULK_STDOUT_ON_WINDOWS = False  # Whether to batch stdout output every 0.1s on Windows (Windows I/O is slow)

DEFAULUT_USE_COLOR_HANDLER = True  # Whether to use colored logging by default.
DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = False  # Whether to use loguru's console handler instead of nb_log's ColorHandler.
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True  # Whether to show block-style background colors in the console.
AUTO_PATCH_PRINT = True  # Whether to auto-patch the print function. When patched, print output gets color and clickable links.

# The following settings control console notification messages.
SHOW_PYCHARM_COLOR_SETINGS = True  # Set to False to suppress PyCharm color optimization tips at startup.
SHOW_NB_LOG_LOGO = True  # Set to False to suppress the nb_log logo at startup.
SHOW_IMPORT_NB_LOG_CONFIG_PATH = True  # Whether to show which nb_log_config.py was loaded.

WHITE_COLOR_CODE = 37  # Different PyCharm versions/themes use either 97 or 37 for white. Adjust as needed.

DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER = False  # Whether to auto-write logs to a file named {namespace}.log even without specifying log_filename.
AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = False  # Whether to auto-write error-level logs to a separate file.
LOG_FILE_SIZE = 1000  # Max file size in MB before rotation.
LOG_FILE_BACKUP_COUNT = 10  # Max number of backup files per log file.

LOG_PATH = os.getenv("LOG_PATH")  # Priority: environment variable. Set LOG_PATH before running your code.
if not LOG_PATH:
    LOG_PATH = '/pythonlogs'  # Default log directory; created at the root of the code's disk if no drive is specified.
    # LOG_PATH = Path(__file__).absolute().parent / Path("pythonlogs")   # Use this to create pythonlogs in your project root.
    if os.name == 'posix':  # Non-root Linux/Mac users can't write to /pythonlogs, so default to ~/pythonlogs.
        home_path = os.environ.get("HOME", '/')
        LOG_PATH = Path(home_path) / Path('pythonlogs')
# print('LOG_PATH:', LOG_PATH)

LOG_FILE_HANDLER_TYPE = 6  # 1 2 3 4 5 6 7 — nb_log's file rotation always ensures multi-process safety.
"""
LOG_FILE_HANDLER_TYPE can be set to 1-7:
1 = Multi-process safe, size-based rotating handler with batch writes.
    Reduces file lock operations; 100x faster on Windows, 5x on Linux vs option 5.
2 = Multi-process safe daily rotation. Same file, new dated file each day.
3 = Non-rotating single file (no rotation = no multi-process issues).
4 = WatchedFileHandler (Linux only, requires logrotate, multi-process safe).
5 = Third-party ConcurrentRotatingFileHandler (file-lock based; OK on Linux with fcntl,
    very slow on Windows with win32con. Prefer option 1 for size-based rotation).
6 = BothDayAndSizeRotatingFileHandler — a fully custom handler that rotates by both time AND size.
7 = LoguruFileHandler — uses loguru's file handler for writing logs.
"""

LOG_LEVEL_FILTER = logging.DEBUG  # Default log level when get_logger doesn't specify one. Logs below this level are discarded.
# It is strongly recommended NOT to raise this globally to INFO.
# Instead, raise the level for specific verbose namespaces individually.

ROOT_LOGGER_LEVEL = logging.INFO  # Root logger level.
ROOT_LOGGER_FILENAME = 'root.log'  # Root logger filename. Set to None to disable file logging for the root logger.
ROOT_LOGGER_FILENAME_ERROR = 'root.error.log'  # Separate error log for the root logger. Set to None to disable.

# Filter words for suppressing console output. If a printed message contains ANY string in FILTER_WORDS_PRINT, it is suppressed.
# Works for both print and logger console output. Useful for silencing noisy third-party package output.
FILTER_WORDS_PRINT = []  # Example: ['annoying_msg', 'skip_this'] — messages containing these strings won't be printed.


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
        log_record[f"{record.__dict__.get('pathname')}:{record.__dict__.get('lineno')}"] = ''
        log_record['ip'] = computer_ip
        log_record['host_name'] = computer_name
        super().add_fields(log_record, record, message_dict)
        if 'for_segmentation_color' in log_record:
            del log_record['for_segmentation_color']


DING_TALK_TOKEN = '3dd0eexxxxxadab014bd604XXXXXXXXXXXX'  # DingTalk alert robot

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
        "%Y-%m-%d %H:%M:%S"),  # A traceback-style template with clickable file location
    4: logging.Formatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
        "%Y-%m-%d %H:%M:%S"),  # Also supports clickable jump
    5: logging.Formatter(
        '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # Recommended template
    6: logging.Formatter('%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
                         "%Y-%m-%d %H:%M:%S"),
    7: logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # Short filename + line number

    8: JsonFormatterJumpAble('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s %(lineno)d  %(process)d %(thread)d', "%Y-%m-%d %H:%M:%S.%f",
                             json_ensure_ascii=False),  # JSON format for ELK stack integration.

    9: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # Template 5 with process and thread IDs.
    10: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # Template 7 with process and thread IDs.
    11: logging.Formatter(
        f'%(asctime)s-({computer_ip},{computer_name})-[p%(process)d_t%(thread)d] - %(name)s - "%(filename)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # Template 7 with process/thread IDs, IP, and hostname.
}

FORMATTER_KIND = 5  # Default formatter template used when get_logger doesn't specify one.

```

The above shows only a partial example of the configuration. All other settings (such as formatter definitions and default template selection) have default values in your project's `nb_log_config.py` — modify them as needed.


### 1.1.1e Relationship Between Config File and get_logger Parameters

`nb_log_config.py` defines global defaults; `get_logger` parameters are per-logger overrides.

For example, if `nb_log_config.py` sets `FORMATTER_KIND = 4` but `get_logger` passes `formatter_template=6`, template 6 will be used.
If `get_logger` doesn't specify a value, the config file setting is used.
In other words, `get_logger` parameters have higher priority than `nb_log_config.py` defaults.



## 1.2 nb_log Features

### 1.2.1 Automatic Color-Coded Logging by Level

Like traffic lights, log colors match intuitive severity levels: green for debug, sky blue for info,
yellow for warning, magenta for error, and dark red for critical.

### 1.2.1b Configuring Color Behavior
nb_log supports automatic coloring, disabling background color blocks while keeping text colors, or disabling all colors entirely.

Modify the relevant settings in your project's auto-generated `nb_log_config.py`:

```
To disable colored logging entirely, set DEFAULUT_USE_COLOR_HANDLER = False
To disable block-style background colors, set DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
To suppress PyCharm color setup tips, set WARNING_PYCHARM_COLOR_SETINGS = False
To change the log template, set FORMATTER_KIND (7 built-in templates, or add custom ones)
LOG_PATH sets the directory for log files.
```

### 1.2.1c How Final Color Rendering Works

Some people have seen blog posts about Python terminal colors, like this one:

[Python print color tutorial](https://www.cnblogs.com/ping-y/p/5897018.html)

```
Python terminals can display 7 ANSI colors simultaneously, but NOT the full 65536-color palette.
PyCharm console, Windows CMD, and Linux terminals are NOT web browsers — they can only expose
7 ANSI color hooks. The terminal software (PyCharm, FinalShell, Xshell, etc.) provides
color customization that maps these 7 ANSI codes to any RGB color in the 65536-color space.

For example, nb_log prints instructions on how to configure these colors at startup.

The key insight: Python's \033[ escape codes only select which of the 7 ANSI color slots to use.
The actual displayed color depends on how your terminal software has mapped those slots.
For example, \033[32 selects "green", but your terminal can map that to any of thousands of
shades of green (or even yellow or purple).

So if you think the colors look ugly, the fix is to customize colors in your terminal software
(PyCharm, Xshell, FinalShell, etc.), not in Python code. It only takes about 30 seconds to set up.
```

### 1.2.1d Precise Color Configuration in PyCharm
```
Note: The same color codes look very different across PyCharm themes. Default themes may look
ugly or produce unreadable text due to poor color contrast.

To achieve optimal color rendering, customize your PyCharm console theme colors.
Instructions are printed in the console at startup, or follow these steps (takes ~30 seconds):

1) In PyCharm: File -> Settings -> Editor -> Color Scheme -> Console Colors
   Select "Monokai" theme, then customize the 7 colors:
   Blue: 0454F3, Cyan: 04DCF8, Green: 13FC02, Magenta: ff1cd5,
   Red: F80606, Yellow: EAFA04, Gray: FFFFFF, White: FFFFFF.
   For background color blocks, depending on your PyCharm version/theme:
   White: 1F1F1F, Black: FFFFFF (dark backgrounds need white text).

2) For Xshell or FinalShell SSH connections, you can also customize theme colors.
   Default shell colors usually work fine as well.
```

### 1.2.2 nb_log Auto-Colors ALL print Statements Project-Wide

```
When nb_log is imported, it monkey-patches the built-in print function.
All print calls throughout your entire project automatically get enhanced behavior,
redirected through nb_log's custom print.
```

### 1.2.2b Benefits of Automatic print Enhancement
```
With automatic print enhancement, you'll never again struggle to find where stray
print statements are coming from.

Just import nb_log, and every print in your project automatically reveals its exact
file and line number with clickable console links.

In a project with hundreds of files, each containing multiple print calls,
it's a nightmare to find specific print output in the console.
For example, someone does print(x) instead of print("value of x:", x),
making it impossible to grep for the source.

Some people suggest commenting out all prints, but that means finding and modifying
potentially thousands of print statements across a large codebase.

With nb_log, all print "ghosts" automatically reveal themselves.

Additionally, using raw print in production code or libraries is considered poor practice.
Professional packages always use proper logging. Logging offers far more flexibility than
print: namespace control, level filtering, template customization, and extensible output
destinations beyond just the console.
```

### 1.2.2c nb_log Colorful Log Output Screenshot


[![pkFSO3V.png](https://s21.ax1x.com/2024/04/29/pkFSO3V.png)](https://imgse.com/i/pkFSO3V)


## 1.3 Clickable Log Links in PyCharm — Jump to Exact File and Line

[![8tka3.png](https://i.postimg.cc/GhRFq5H9/8tka3.png)](https://postimg.cc/w3WRBF5d)

## 1.4 nb_log Uses Native logging — Excellent Compatibility and Extensibility

nb_log is built on Python's built-in `logging` module. `nb_log.get_logger()` returns a native `logging.Logger` instance, achieving 100% compatibility with third-party packages.

Whether the logger type is native `logging.Logger` matters a great deal. logbook and loguru are NOT native logging, so they have poor compatibility with third-party packages for drop-in replacement.

```
Libraries like loguru and logbook implement their own logging from scratch.
Their main logger objects are not Python's built-in Logger type,
meaning some attributes and methods may be missing or behave differently.
This makes them poorly compatible with Python's standard logging —
they can only handle simple method replacements like debug/info/warning/error.
```

## 1.5 nb_log Can Easily Log to Any Combination of 10+ Destinations

Built-in one-parameter switches allow you to log to any combination of 10+ common destinations:
console, file, DingTalk, email, MongoDB, Kafka, Elasticsearch, and more.

Some people think logging can only go to the console and files — that's wrong. Where logs go depends on which handlers you add to the logger.


## 1.6 Independent Logger Namespaces with Multi-Instance Loggers

```python
"""
Independent namespaces mean each logger has its own level filtering
and its own set of output destinations.
"""

from nb_log import get_logger, LogManager

logger_aa = LogManager('aa').get_logger_and_add_handlers(10, log_filename='aa.log')
logger_bb = get_logger("bb", log_level_int=30, is_add_stream_handler=False, ding_talk_token='your_dingding_token')
logger_cc = get_logger('cc', log_level_int=10, log_filename='cc.log')

logger_aa.debug('hahaha')
# Written to both console and aa.log. Debug and above are recorded.

logger_bb.warning('heyhey')
# Only sent to DingTalk. logger_bb's info and debug are filtered out.
# Very convenient for development — debug freely, then raise the level for production.

logger_cc.debug('hehe')
# logger_cc's logs go to cc.log — a separate file from logger_aa.
```

Logger namespaces are crucial. Some people set the level to `logging.WARN` but find debug logs still appearing — that's because they didn't pay attention to WHICH namespace the level was set on vs. which namespace produced the debug output.

Search this document for "namespace" and you'll find it mentioned hundreds of times. Some developers have such weak understanding of the `logging` module that extensive explanation is needed here, which is why this document is so long.



## 1.7 Monkey-Patched logging: No Duplicate Handler Records

```
from logging import getLogger, StreamHandler
logger = getLogger('hi')
getLogger('hi').addHandler(StreamHandler())
getLogger('hi').addHandler(StreamHandler())
getLogger('hi').addHandler(StreamHandler())
logger.warning('lalala')

Even though warning was called only once, "lalala" prints 3 times to the console.
With nb_log, you can fearlessly add the same handler type to the same namespace multiple times
without duplicate log entries.

Even worse duplicate-logging scenarios are shown later in this document,
where they can exhaust CPU and fill up disk space.
```

## 1.8 nb_log Is Simpler Than Both Native logging and loguru

### 1.8.1 Creating a Logger with Code (Native logging)

```python
import logging
logger = logging.getLogger('my.logger.namespace')

fh = logging.FileHandler('test.log')  # Write to file

ch = logging.StreamHandler()  # Write to console

fm = logging.Formatter('%(asctime)s %(message)s')  # Format template

fh.setFormatter(fm)
ch.setFormatter(fm)

logger.addHandler(fh)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)  # Set level


logger.debug('debug message')

```

Many people are intimidated by native logging. Creating a proper logger object requires complex setup steps: creating observer handlers, setting formatters, and adding observers to the subject.
Most people haven't studied design patterns, don't understand (or haven't even heard of) the Observer pattern, so this setup is bewildering.

The step-by-step approach exists to give users maximum flexibility. High-level encapsulation is simpler but reduces customization.

Since logging is Python's built-in module and every third-party package uses it, you MUST learn logging for compatibility. Trying to avoid it by using only loguru doesn't work — third-party packages don't use loguru.

nb_log encapsulates the logger creation process while exposing many `get_logger` parameters for user-defined customization of handlers and formatters. So nb_log has the universal compatibility of native logging AND the simplicity of modern alternatives.


### 1.8.2 Creating a Logger with logging.config.dictConfig()

```python
import logging
import logging.config
 
LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            'format':'%(asctime)s %(filename)s %(lineno)s %(levelname)s %(message)s',
        },
        "plain": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
        "console_plain": {
            "class": "logging.StreamHandler",
            "level":logging.INFO,
            "formatter": "plain"
        },
        "file":{
            "class": "logging.FileHandler",
            "level":20,
            "filename": "./log.txt",
            "formatter": "default",
        }
    },
    "loggers": {
        "console_logger": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "console_plain_file_logger": {
            "handlers": ["console_plain","file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "file_logger":{
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        }
    },
    "disable_existing_loggers": True,
}
 
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("console_logger")
logger.debug('debug message')
logger.info('info message')
logger.warn('warning message')
logger.error('error message')
logger.critical('critical message')


```

Similar to section 1.8.1, but replaces Python code with a `LOGGING_CONFIG` dictionary.
While you don't need to write verbose Python code to construct loggers, you do need to write this config dict — mistakes in the dict cause silent failures or errors. Many people find this configuration baffling.

The process: create formatters, create file/console handlers (or custom handlers like DingTalk), set handler levels and formatters (different handlers can use different formatters — the same `logger.debug("hello world")` can have different prefixes in file vs console output).

Different logger namespaces get different handlers:
- Want console-only? Use `logger = logging.getLogger("console_logger")`
- Want file-only? Use `logger = logging.getLogger("file_logger")`
- Want both? Use `logger = logging.getLogger("console_plain_file_logger")`


The complexity of 1.8.1 and 1.8.2 is the main reason people flock to loguru.


### 1.8.3 Simple loguru Usage

```python
from loguru import logger
logger.add("./log_files/loguru-test1.log",  rotation="100000 KB")
logger.info("hello")
```

```
This logs to both console and file — just as concise as nb_log.
If you don't need file output, just import and go:

from loguru import logger
logger.info("hello")

Looks simple. nb_log requires a get_logger call, and some people think loguru is better
because it saves one line of code. But nb_log also supports import-and-use:

from nb_log import defaul_logger
defaul_logger.info("hello")

The downside: you can't customize templates, choose which destinations to log to
(console, file, DingTalk, ES), or independently control different functions' log levels.
If you want to suppress logs from function_a but keep logs from function_b,
a single shared logger without namespace separation can't do that.

That's why nb_log recommends calling get_logger to create custom loggers
rather than using a single pre-built logger everywhere.
```

### 1.8.4 nb_log Can Be Even Simpler Than loguru

loguru:
```
from loguru import logger
logger.add("./log_files/loguru-test1.log",  rotation="100000 KB")
logger.info("hello")
```

nb_log — if you want something quick and don't want to call get_logger:
```
import nb_log

nb_log.debug('For those who prefer not to instantiate named loggers and just want direct function calls')
nb_log.info('For those who prefer not to instantiate named loggers and just want direct function calls')
nb_log.warning('For those who prefer not to instantiate named loggers and just want direct function calls')
nb_log.error('For those who prefer not to instantiate named loggers and just want direct function calls')
nb_log.critical('For those who prefer not to instantiate named loggers and just want direct function calls')

```

[![pPSPUDs.png](https://s1.ax1x.com/2023/07/28/pPSPUDs.png)](https://imgse.com/i/pPSPUDs)

```
For those who don't understand the power of logging.getLogger's name parameter
and find instantiating named loggers "too much work" — nb_log accommodates you.

Using loguru-style logging (from loguru import logger) makes it difficult to
set different log levels for different modules, or write different modules'
logs to different files. It's messy and inelegant.

But for those who just don't get namespaces and complain about instantiation:

import nb_log

nb_log.debug('For those who just want to call debug() directly')
nb_log.info('For those who just want to call info() directly')

loguru usage:
from loguru import logger
logger.debug(msg)

nb_log usage:
import nb_log
nb_log.debug(msg)

nb_log doesn't even need from/import — just a plain import. Even simpler!
```



In summary, nb_log is both simple to use AND highly compatible.

## 1.9 What Is a logging Namespace?

```python
import logging
logger1 = logging.getLogger('aaa')

logger2 = logging.getLogger('aaa')

logger3 = logging.getLogger('bbb')

print('logger1 id: ', id(logger1), 'logger2 id: ', id(logger2), 'logger3 id: ', id(logger3))
```

Running this reveals that logger1 and logger2 are the same object (same id), while logger3 is different.
Different namespaces allow setting different log levels, writing to different files, controlling console output, and choosing whether to send emails or DingTalk messages.

<pre style="font-size: large;color: #FFFF66;background-color: #0c1119">
Some developers still don't understand what namespaces do, treating ALL logs in a large project
with identical behavior. If someone says "the logs are too verbose, raise the log level",
that's an amateur approach. How do you raise the level? Without understanding namespaces,
you simply can't do it properly.

If you raise the level globally, what about the other module where you need debug output?
You only want to suppress SOME debug logs, not all of them.
</pre>

### 1.9.2 Experts vs Beginners: Logging Flask Requests and Errors

#### 1.9.2.a Beginner Approach: Manually Logging Flask Requests (Redundant Work)
```python
"""
1) Manually logging request params and URLs inside endpoints — completely redundant.
2) Manually logging Flask endpoint errors inside try/except.

Even if you add logging at the framework level or via decorators,
it's still a poor approach.

Without understanding namespaces, you're duplicating work that
the framework already does — it just hasn't added handlers yet,
waiting for the user to add them.
"""
import traceback
from flask import Flask, request
from loguru import logger

app = Flask(__name__)

logger.add('mylog.log')


@app.route('/')
def hello():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr)  # Redundant!
    return 'Hello World!'


@app.route('/api2')
def api2():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr)
    try:
        1 / 0  # Intentional error
        return '2222'
    except Exception as e:
        logger.error(f'e {traceback.format_exc()}')  # Redundant!


if __name__ == '__main__':
    app.run()

```

#### 1.9.2.b Expert Approach: Zero Manual Logging Code Needed
```python
"""
This code contains ZERO manual logging of Flask requests or errors,
yet everything is automatically recorded. This is what namespace mastery looks like.

The correct approach: add handlers to the 'werkzeug' namespace.
Any request automatically gets logged to console and werkzeug.log.

Flask reuses app.name as its logging namespace.
So adding handlers to 'myapp' means Flask endpoint errors
are automatically logged with full stack traces to myapp.log and console.
"""

from flask import Flask, request
import nb_log

app = Flask('myapp')

nb_log.get_logger('werkzeug', log_filename='werkzeug.log')

nb_log.get_logger('myapp', log_filename='myapp.log')


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/api2')
def api2():
    1 / 0
    return '2222'


if __name__ == '__main__':
    app.run(port=5002)
```

```
This comparison shows how much redundant work you do when you don't understand namespaces.
```

How did I know to use the 'werkzeug' and 'myapp' namespaces?

```
I didn't cheat by Googling first.

nb_log.get_logger(name=None) captures ALL logging output from any namespace.
Set name=None first, and the console template shows the namespace for each log entry.
Then you'll know exactly which namespaces to target.
```

## 1.10 nb_log Has 10 Advantages Over loguru

[nb_log's 10 advantages over loguru](https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c6.html)


## 1.10.b nb_log Now Supports Native loguru Mode

Pass `is_use_loguru_stream_handler=True` to `get_logger` (or set `DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = True` in `nb_log_config.py`) to use loguru for console output.

Pass `log_file_handler_type=7` to `get_logger` (or set `LOG_FILE_HANDLER_TYPE = 7` in `nb_log_config.py`) to use loguru's file handler for writing logs.


Using nb_log with loguru makes it trivial to write function_a's logs to file_a and function_b's logs to file_b.

Example:

```python
import time

import nb_log

logger = nb_log.get_logger('name1', is_use_loguru_stream_handler=True, log_filename='testloguru_file111.log', log_file_handler_type=7)
logger2 = nb_log.get_logger('name2', is_use_loguru_stream_handler=True, log_filename='testloguru_file222.log', log_file_handler_type=7)

for i in range(10000000000):
    logger.debug('loguru debug 111111')
    logger2.debug('loguru debug 222222')

    logger.info('loguru info 111111')
    logger2.info('loguru info 222222')

    logger.warning('loguru warn 111111')
    logger2.warning('loguru warn 22222 ')

    logger.error('loguru err 1111111')
    logger2.error('loguru err 2222222')

    logger.critical('loguru critical 111111')
    logger2.critical('loguru caritical 222222')

    time.sleep(1)

import requests

# By adding loguru handlers to the relevant namespaces, nb_log makes loguru
# automatically capture logging output from third-party libs like django, flask, requests, urllib3.
# Doing this with pure loguru is difficult, but with nb_log's loguru mode, it's trivial.
nb_log.get_logger('urllib3', is_use_loguru_stream_handler=True)

requests.get('http://www.baidu.com')  


time.sleep(100000)
```

Some people used to question whether nb_log is as good as loguru. Now that nb_log fully supports loguru, what's left to question?

It's like the funboost framework — when people questioned it, funboost added Celery as a broker, fully leveraging Celery's scheduling core, and made it simpler than using Celery directly.

The author has always been inclusive of third-party frameworks: if I can't convince you, I'll integrate your tool instead.

## 1.11 About Setting nb_log Log Levels — See Section 9.5

Understanding the first parameter of `logging.getLogger()` is critically important.

[About setting nb_log log levels](https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c9.html#id2)

## 1.20 Full Documentation

[nb_log readthedocs documentation](https://nb-log-doc.readthedocs.io/zh_CN/latest)

[nb_log source code](https://github.com/ydf0509/nb_log)

![](https://visitor-badge.glitch.me/badge?page_id=nb_log)

<div> </div>
