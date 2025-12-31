# 🤖 AI Reading Guide for Project: nb_log

> **Important Notice for AI Models**: This document contains the complete source code and documentation for the `nb_log` project. Please read this guide carefully before analyzing the content.

## 📖 Document Structure

This markdown document is structured as follows:

1. **Project Summary** (`# markdown content namespace: xxx project summary`)
   - Brief project description
   - Core source files metadata (AST-parsed class/function signatures without full source code)
   - File dependencies analysis

2. **Project Root Files** (`# markdown content namespace: xxx Project Root Dir Some Files`)
   - README.md, pyproject.toml, setup.py, etc.

3. **Source Code Sections** (`# markdown content namespace: xxx codes/examples/...`)
   - File Tree: Shows directory structure
   - Included Files: Lists all files in this section
   - Full source code with AST metadata for Python files

## 🔍 How to Identify File Boundaries

- Each file starts with: `--- **start of file: <path>** (project: nb_log) ---`
- Each file ends with: `--- **end of file: <path>** (project: nb_log) ---`
- All file paths are relative to the project root

## ⚠️ Important Notes

1. **Do NOT hallucinate**: Only reference code, classes, functions, and APIs that actually exist in this document
2. **Check file paths**: When suggesting code changes, always verify the file path exists in the File Tree
3. **Respect the project structure**: The File Tree shows the actual directory layout
4. **AST Metadata**: Python files include parsed metadata (imports, classes, methods) before the full source code

---

# markdown content namespace: nb_log project summary 



- `nb_log` is a powerful logging library for Python. 

- `nb_log.get_logger(...)` is the main function to get a logger object.
   get_logger 入参非常重要，不可以胡乱编造入参。

- nb_log_config.py 是nb_log的配置文件，非常重要，不可以胡乱编造配置名称。



## 📋 nb_log most core source files metadata (Entry Points)


以下是项目 nb_log 最核心的入口文件的结构化元数据，帮助快速理解项目架构：



### the project nb_log most core source code files as follows: 
- `nb_log/__init__.py`
- `nb_log/log_manager.py`
- `nb_log/nb_log_config_default.py`


### 📄 Python File Metadata: `nb_log/__init__.py`

#### 📦 Imports

- `import logging`
- `import warnings`
- `import nb_log.add_python_executable_dir_to_path_env`
- `from nb_log.set_nb_log_config import use_config_form_nb_log_config_module`
- `from nb_log import nb_log_config_default`
- `from nb_log.monkey_sys_std import patch_sys_std`
- `from nb_log.monkey_sys_std import stderr_raw`
- `from nb_log.monkey_sys_std import stdout_raw`
- `from nb_log.monkey_std_filter_words import patch_std_filter_words`
- `from nb_log.monkey_print import nb_print`
- `from nb_log.monkey_print import patch_print`
- `from nb_log.monkey_print import reverse_patch_print`
- `from nb_log.monkey_print import stdout_write`
- `from nb_log.monkey_print import stderr_write`
- `from nb_log.monkey_print import print_raw`
- `from nb_log.monkey_print import is_main_process`
- `from nb_log.monkey_print import only_print_on_main_process`
- `from nb_log.helpers import generate_error_file_name`
- `from nb_log import handlers`
- `from nb_log.log_manager import LogManager`
- `from nb_log.log_manager import LoggerLevelSetterMixin`
- `from nb_log.log_manager import LoggerMixin`
- `from nb_log.log_manager import LoggerMixinDefaultWithFileHandler`
- `from nb_log.log_manager import FileLoggerMixin`
- `from nb_log.log_manager import MetaTypeLogger`
- `from nb_log.log_manager import MetaTypeFileLogger`
- `from nb_log.log_manager import get_logger`
- `from nb_log.log_manager import get_logger_with_filehanlder`
- `from nb_log.loggers_imp.compatible_logger import CompatibleLogger`
- `from nb_log import global_except_hook`
- `from nb_log.exception_auto_log import LogException`
- `from nb_log.root_logger import root_logger`
- `from nb_log.capture_warnings import capture_warnings_with_frequency_control`
- `from nb_log.direct_logger import debug`
- `from nb_log.direct_logger import info`
- `from nb_log.direct_logger import warning`
- `from nb_log.direct_logger import error`
- `from nb_log.direct_logger import exception`
- `from nb_log.direct_logger import critical`


---




### 📄 Python File Metadata: `nb_log/log_manager.py`

#### 📝 Module Docstring

`````
日志管理，支持日志打印到控制台和写入切片文件和mongodb和email和钉钉机器人和elastic和kafka。
建造者模式一键创建返回添加了各种好用的handler的原生官方Logger对象，兼容性扩展性极强。
使用观察者模式按照里面的例子可以扩展各种有趣的handler。
使用方式为  logger = LogManager('logger_name').get_and_add_handlers(log_level_int=1, is_add_stream_handler=True,
 log_path=None, _log_filename=None, log_file_size=10,mongo_url=None,formatter_template=2)


concurrent_log_handler的ConcurrentRotatingFileHandler解决了logging模块自带的RotatingFileHandler多进程切片错误，
此ConcurrentRotatingFileHandler在win和linux多进程场景下log文件切片都ok.

1、根据日志级别，使用coolorhanlder代替straemhandler打印5种颜色的日志，一目了然哪里是严重的日志。
2、带有多种handler，邮件 mongo stream file的。
3、支持pycharm点击日志跳转到对应代码文件的对应行。
4、对相同命名空间的logger可以无限添加同种类型的handlers，不会重复使用同种handler记录日志。不需要用户自己去判断。
5、更新文件日志性能，基于ConcurrentRotatingFileHandler继承重写，使用缓存1秒内的消息成批量的方式插入，
使极限多进程安全切片的文件日志写入性能在win下提高100倍，linux下提高10倍。
`````

#### 📦 Imports

- `import logging`
- `import multiprocessing`
- `import threading`
- `import typing`
- `from functools import lru_cache`
- `from logging import FileHandler`
- `from logging import _checkLevel`
- `from nb_log import nb_log_config_default`
- `from nb_log.loggers_imp.compatible_logger import CompatibleLogger`
- `from nb_log.handlers import *`
- `import deprecated`
- `from nb_log.helpers import generate_error_file_name`
- `from nb_log.handlers_more import MongoHandler`
- `from nb_log.handlers_more import ElasticHandler`
- `from nb_log.handlers_more import KafkaHandler`
- `from nb_log.handlers_loguru import LoguruStreamHandler`
- `from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos`
- `from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandlerWithBufferInitiativeLinux`
- `from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandler`
- `from nb_log.handlers_loguru import LoguruFileHandler`

#### 🏛️ Classes (10)

##### 📌 `class _Undefind`
*Line: 155*

##### 📌 `class DataClassBase`
*Line: 163*

**Docstring:**
`````
使用类实现的
相比与字典，数据类在ide下补全犀利。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, **kwargs)`
  - **Parameters:**
    - `self`
    - `**kwargs`

**Public Methods (2):**
- `def get_dict(self)`
- `def get_json(self)`

##### 📌 `class MailHandlerConfig(DataClassBase)`
*Line: 197*

**Class Variables (9):**
- `mailhost: tuple = nb_log_config_default.EMAIL_HOST`
- `fromaddr: str = nb_log_config_default.EMAIL_FROMADDR`
- `toaddrs: tuple = nb_log_config_default.EMAIL_TOADDRS`
- `subject: str = 'xx项目邮件日志报警'`
- `credentials: tuple = nb_log_config_default.EMAIL_CREDENTIALS`
- `secure = None`
- `timeout = 5.0`
- `is_use_ssl = True`
- `mail_time_interval = 60`

##### 📌 `class LogManager(object)`
*Line: 230*

**Docstring:**
`````
一个日志管理类，用于创建logger和添加handler，支持将日志打印到控制台打印和写入日志文件和mongodb和邮件。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, logger_name: typing.Union[str, None] = 'nb_log_default_namespace', logger_cls = logging.Logger)`
  - **Docstring:**
  `````
  :param logger_name: 日志名称，当为None时候创建root命名空间的日志，一般情况下千万不要传None，除非你确定需要这么做和是在做什么.这个命名空间是双刃剑
  `````
  - **Parameters:**
    - `self`
    - `logger_name: typing.Union[str, None] = 'nb_log_default_namespace'`
    - `logger_cls = logging.Logger`

**Public Methods (8):**
- `def get_all_logging_name()` `staticmethod`
- `def preset_log_level(self, log_level_int = 20)`
  - **Docstring:**
  `````
  提前设置锁定日志级别，当之后再设置该命名空间日志的级别的时候，按照提前预设的级别，无视之后设定的级别。
  主要是针对动态初始化的日志，在生成日志之后再去设置日志级别不方便。
  :param log_level_int:logging.DEBUG LOGGING.INFO 等
  :return:
  `````
- `def prevent_add_handlers(self)`
  - *对命名空间设置阻止添加handlers*
- `def get_logger_and_add_handlers(self, log_level_int: int = None) -> logging.Logger`
  - **Docstring:**
  `````
  :param log_level_int: 日志输出级别，设置为 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，
  :param is_add_stream_handler: 是否打印日志到控制台
  :param is_use_loguru_stream_handler  是否使用 loguru的控制台打印，如果为None，使用 nb_log_config.py的DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER 值。
  :param do_not_use_color_handler :是否禁止使用color彩色日志
  :param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
         非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
  :param log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
  :param error_log_filename :错误日志文件名字，如果文件名不为None，那么error级别以上日志自动写入到这个错误文件。
  :param log_file_size :日志大小，单位M，默认100M
  :param log_file_handler_type :这个值可以设置为1 2 3 4 5 6 7，1为使用多进程安全按日志文件大小切割的文件日志
         2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
         3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
         4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
         5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
           这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
         6 为作者发明的高性能多进程安全，同时按大小和时间切割的文件日志handler
         7 为 loguru的 文件日志记录器
  :param mongo_url : mongodb的连接，为None时候不添加mongohandler
  :param is_add_elastic_handler: 是否记录到es中。
  :param is_add_kafka_handler: 日志是否发布到kafka。
  :param ding_talk_token:钉钉机器人token
  :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
  :param mail_handler_config : 邮件配置
  :param is_add_mail_handler :是否发邮件
  :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                           1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                           如果为logging.Formatter对象，则直接使用用户传入的模板。
  :type log_level_int :int
  :type is_add_stream_handler :bool
  :type log_path :str
  :type log_filename :str
  :type mongo_url :str
  :type log_file_size :int
  `````
- `def get_logger_without_handlers(self)`
  - *返回一个不带hanlers的logger*
- `def look_over_all_handlers(self)`
- `def remove_all_handlers(self)`
- `def remove_handler_by_handler_class(self, handler_class: typing.Union[type, str])`
  - **Docstring:**
  `````
  去掉指定类型的handler
  :param handler_class:logging.StreamHandler,ColorHandler,MongoHandler,ConcurrentRotatingFileHandler,MongoHandler,CompatibleSMTPSSLHandler的一种
  :return:
  `````

**Class Variables (4):**
- `logger_name_list = []`
- `logger_list = []`
- `preset_name__level_map = dict()`
- `logger_name__logger_cls_obj_map = {}`

##### 📌 `class LoggerLevelSetterMixin`
*Line: 614*

**Public Methods (1):**
- `def set_log_level(self, log_level = 10)`

##### 📌 `class LoggerMixin(LoggerLevelSetterMixin)`
*Line: 625*

**Docstring:**
`````
主要是生成把类名作为日志命名空间的logger，方便被混入类直接使用self.logger，不需要手动实例化get_logger。
`````

**Properties (3):**
- `@property logger_full_name`
- `@property logger -> logging.Logger`
- `@property logger_with_file -> logging.Logger`

**Class Variables (2):**
- `subclass_logger_dict = {}`
- `logger_extra_suffix = ''`

##### 📌 `class LoggerMixinDefaultWithFileHandler(LoggerMixin)`
*Line: 661*

**Properties (1):**
- `@property logger`

**Class Variables (1):**
- `subclass_logger_dict = {}`

##### 📌 `class MetaTypeLogger(type)`
*Line: 679*

**🔧 Constructor (`__init__`):**
- `def __init__(cls, name, bases, attrs)`
  - **Parameters:**
    - `cls`
    - `name`
    - `bases`
    - `attrs`

##### 📌 `class MetaTypeFileLogger(type)`
*Line: 685*

**🔧 Constructor (`__init__`):**
- `def __init__(cls, name, bases, attrs)`
  - **Parameters:**
    - `cls`
    - `name`
    - `bases`
    - `attrs`

##### 📌 `class LoggedException(Exception)`
*Line: 714*

**Docstring:**
`````
抛出异常的同时,自动记录日志到日志文件中,这样就不需要每次都raise,并写日志日路,分两行来写了.
try :
    1/0
except Exception as e:
    raise LoggedException(message='有问题',)
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, message: str, logger_obj = None, exc_info = True)`
  - **Docstring:**
  `````
  :param message:
  :param logger_obj: 传递logger对象,使用指定的logger来记录日志,那就log_filename不起作用
  :param exc_info: 日志是否记录仪详细报错堆栈
  `````
  - **Parameters:**
    - `self`
    - `message: str`
    - `logger_obj = None`
    - `exc_info = True`

#### 🔧 Public Functions (11)

- `def revision_call_handlers(self, record)`
  - *Line: 46*
  - **Docstring:**
  `````
  重要。这可以使同名logger或父logger随意添加同种类型的handler，确保不会重复打印。
  例如对"a"命名空间加上streamhandler，对"a.b"命名空间也加上streamhandler，则"a.b"命名空间的日志会被打印两次
  例子如下
  
  import logging
  
  logger1 = logging.getLogger('a')
  logger1.addHandler(logging.StreamHandler())
  
  logger2 = logging.getLogger('a.b')
  logger2.addHandler(logging.StreamHandler())
  
  logger2.error(666)
  
  明明只想打印一次666，结果却答应2次了。因为a.b的父命名空间的日志也加了streamhandler。
  
  :param self:
  :param record:
  :return:
  `````

- `def revision_add_handler(self, hdlr)`
  - *Line: 109*
  - *Add the specified handler to this logger.*

- `def revision_setLevel(self, level)`
  - *Line: 134*
  - *Set the logging level of this logger.  level must be an int or a str.*

- `def get_all_logging_name()`
  - *Line: 209*

- `def get_all_handlers()`
  - *Line: 214*

- `def check_log_level(log_level: int)`
  - *Line: 224*

- `def get_logger(name: typing.Union[str, None]) -> logging.Logger` `lru_cache()`
  - *Line: 545*
  - **Docstring:**
  `````
  重写一遍，是为了更好的pycharm自动补全，所以不用**kwargs的写法。
  如果太喜欢函数调用了，可以使用这种.
  get_logger_and_add_handlers是LogManager类最常用的公有方法，其他方法使用场景的频率比较低，
  但如果要使用那些低频率功能，还是要亲自调用LogManger类，而不是仅仅只了解此函数的用法。
      :param name 日志命名空间，这个是最重要最难理解的一个入参，很多pythoner到现在还不知道name是什么作用。日志命名空间，意义非常非常非常重要，有些人到现在还不知道 logging.getLogger() 第一个入参的作用，太low了。不同的name的logger可以表现出不同的行为。
              例如让 aa命名空间的日志打印控制台并且写入到文件，并且只记录info级别以上，让 bb 命名空间的日志仅仅打印控制台，并且打印debug以上级别，
              这种就可以通过不同的日志命名空间做到。
      :param log_level_int: 日志输出级别，设置为 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，现在可以直接用10 20 30 40 50了，兼容了。
     :param is_add_stream_handler: 是否打印日志到控制台
     :param is_use_loguru_stream_handler  是否使用 loguru的控制台打印，如果为None，使用 nb_log_config.py的DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER 值。
     :param do_not_use_color_handler :是否禁止使用color彩色日志
     :param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
            非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
     :param log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
     :param error_log_filename :错误日志文件名字，如果文件名不为None，那么error级别以上日志自动写入到这个错误文件。
     :param log_file_size :日志大小，单位M，默认100M
     :param log_file_handler_type :这个值可以设置为1 2 3 4 5 6 7，1为使用多进程安全按日志文件大小切割的文件日志
            2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
            3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
            4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
            5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
              这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
            6 为作者发明的高性能多进程安全，同时按大小和时间切割的文件日志handler
            7 为 loguru的 文件日志记录器
     :param mongo_url : mongodb的连接，为None时候不添加mongohandler
     :param is_add_elastic_handler: 是否记录到es中。
     :param is_add_kafka_handler: 日志是否发布到kafka。
     :param ding_talk_token:钉钉机器人token
     :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
     :param mail_handler_config : 邮件配置
     :param is_add_mail_handler :是否发邮件
     :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                              1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                              如果为logging.Formatter对象，则直接使用用户传入的模板。
     :type log_level_int :int
     :type is_add_stream_handler :bool
     :type log_path :str
     :type log_filename :str
     :type mongo_url :str
     :type log_file_size :int
  `````

- `def get_logger_with_filehanlder(name: str) -> logging.Logger` `lru_cache()`
  - *Line: 605*
  - **Docstring:**
  `````
  默认添加color handler  和 文件日志。
  :param name:
  :return:
  `````

- `def logger_catch(logger: logging.Logger, reraise: bool = True, show_trace_back = True)`
  - *Line: 691*

- `def build_exception_logger()` `lru_cache()`
  - *Line: 709*

- `def logged_raise(e: BaseException, logger_obj = None, exc_info = True)`
  - *Line: 740*
  - **Docstring:**
  `````
  try :
      1/0
  except Exception as e:
      logged_raise(ZeroDivisionError('0不能是被除数'))
  
  :param e:
  :param logger_obj:
  :param exc_info:
  :return:
  `````


---




### 📄 Python File Metadata: `nb_log/nb_log_config_default.py`

#### 📝 Module Docstring

`````
此文件nb_log_config.py是自动生成到python项目的根目录的,因为是自动生成到 sys.path[1]。
在这里面写的变量会覆盖此文件nb_log_config_default中的值。对nb_log包进行默认的配置。用户是无需修改nb_log安装包位置里面的配置文件的。

但最终配置方式是由get_logger_and_add_handlers方法的各种传参决定，如果方法相应的传参为None则使用这里面的配置。
`````

#### 📦 Imports

- `import sys`
- `import logging`
- `import os`
- `from pathlib import Path`
- `import socket`
- `from pythonjsonlogger.jsonlogger import JsonFormatter`

#### 🏛️ Classes (1)

##### 📌 `class JsonFormatterJumpAble(JsonFormatter)`
*Line: 109*

**Public Methods (1):**
- `def add_fields(self, log_record, record, message_dict)`

#### 🔧 Public Functions (1)

- `def get_host_ip()`
  - *Line: 91*


---



## 🔗 nb_log Some File Dependencies Analysis

以下是项目文件之间的依赖关系，帮助 AI 理解代码结构：

### 📊 Internal Dependencies Graph

`````
Entry Points (not imported by other project files):
  ★ nb_log/nb_log_config_default.py

Core Files (imported by other files, sorted by import count):
  ◆ nb_log/__init__.py (imported by 1 files)
  ◆ nb_log/log_manager.py (imported by 1 files)

`````

### 📋 Detailed Dependencies

#### `nb_log/__init__.py`

**Imports from project:**
- `nb_log/log_manager.py`

**Imported by:**
- `nb_log/log_manager.py`

#### `nb_log/log_manager.py`

**Imports from project:**
- `nb_log/__init__.py`

**Imported by:**
- `nb_log/__init__.py`

### 📦 Third-party Dependencies

项目使用的第三方库：

- `deprecated`
- `pythonjsonlogger`
- ......以及更多的第三方库......


---
# markdown content namespace: nb_log docs 


## nb_log File Tree (relative dir: `source/articles`)


`````

└── source
    └── articles
        ├── c1.md
        ├── c10.md
        ├── c2.md
        ├── c3.md
        ├── c4.md
        ├── c5.md
        ├── c6.md
        ├── c7.md
        ├── c8.md
        └── c9.md

`````

---


## nb_log (relative dir: `source/articles`)  Included Files (total: 10 files)


- `source/articles/c1.md`

- `source/articles/c10.md`

- `source/articles/c2.md`

- `source/articles/c3.md`

- `source/articles/c4.md`

- `source/articles/c5.md`

- `source/articles/c6.md`

- `source/articles/c7.md`

- `source/articles/c8.md`

- `source/articles/c9.md`


---


--- **start of file: source/articles/c1.md** (project: nb_log) --- 

`````markdown

# 1.nb_log 简介

[nb_log readthedocs文档链接](https://nb-log-doc.readthedocs.io/zh_CN/latest)

[nb_log 源码链接](https://github.com/ydf0509/nb_log)

[//]: # ([![image.png]&#40;https://i.postimg.cc/ydqgWDRW/image.png&#41;]&#40;https://postimg.cc/HJ2shsBC&#41;)

[![pkFSfc8.png](https://s21.ax1x.com/2024/04/29/pkFSfc8.png)](https://imgse.com/i/pkFSfc8)



文中文档较长，但其中大部分不是 讲解nb_log 的用法，是复习内置logging的概念。
是由于python人员不懂logging包的日志命名空间和python日志树形命名空间结构，不懂handlers和logger的关系是什么。
所以需要很长的篇幅。

很多pythoner到现在都不知道python的 logging.getLogger() 第一个入参的意义和作用，造成nb_log也不知道怎么使用多命名空间。

## tips: 要想更简单简化使用日志,请安装kuai_log

pip install kuai_log

```
kuai_log 是没有基于logging封装,但kuai_log是100%兼容logging包的方法名和入参.
kuai_log的KuaiLogger方法和入参在logging的Logger一定存在且相同, 但是logging包有的小众方法,kuai_log不存在

kuai_log比logging和loguru快30倍,比nb_log快4倍.

kuai_log 不需要配置文件,全部用入参

kuai_log 没有依赖任何三方包,nb_log依赖某些三方包

```

## nb_log  logging loguru 快速比较

| 维度     | loguru  | logging | nb\_log           |
| ------ | ------- | ------- | ----------------- |
| 易用性    | ✅ 简单    | ❌ 繁琐    | ✅ 简单              |
| 命名空间   | ❌ 无     | ✅ 完善    | ✅ 完善              |
| 第三方库兼容 | ❌ 容易污染  | ✅ 安全    | ✅ 安全              |
| 美化输出   | ✅ 默认很好看 | ❌ 需配置   | ✅ 默认美观            |
| 拓展性    | ⚠️ 不够灵活 | ✅ 高     | ✅ 更高（支持多 handler） |
| 上手体验   | ✅ 快速爽   | ❌ 枯燥复杂  | ✅ 一秒用上好日志         |


## 1.0 nb_log 安装

pip install nb_log

## 1.0.1 nb_log不仅是日志，还对print以及sys.stdout(sys.stderr) 打了强力的猴子补丁

对代码里面的print打了猴子补丁，自动显示print所在地方的文件名和精确行号，不怕有人胡乱print，找不到在哪里print的了。

对代码里面的 print 以及 streamHanlder日志调用的sys.stdout/stderr 打了猴子补丁，能支持所有标准输出自动写入到文件中,每天生成一个文件。
(见1.1.d配置文件说明的 SYS_STD_FILE_NAME 和 PRINT_WRTIE_FILE_NAME)。


## 1.0.2 nb_log 新增支持loguru包模式来记录日志，原汁原味的loguru来打印控制台和写入日志文件，见文档1.10.b

有了这，还有什么理由还说nb_log不如loguru，loguru只是nb_log的一个子集。

loguru控制台打印模式截图:
[![pkFShjS.png](https://s21.ax1x.com/2024/04/29/pkFShjS.png)](https://imgse.com/i/pkFShjS)

## 1.1 nb_log 简单使用例子

控制台打印日志：

```python
print('导入nb_log之前的print是普通的')

from nb_log import get_logger

logger = get_logger('lalala',)   # get_logger 只有一个name是必传递的，其他的参数不是必传。
# logger = get_logger('lalala',log_filename='lalala.log',formatter_template=5,log_file_handler_type=2) # get_logger有很多其他入参可以自由定制logger。


logger.debug(f'debug是绿色，说明是调试的，代码ok ')
logger.info('info是天蓝色，日志正常 ')
logger.warning('黄色yello，有警告了 ')
logger.error('粉红色说明代码有错误 ')
logger.critical('血红色，说明发生了严重错误 ')

print('导入nb_log之后的print是强化版的可点击跳转的')
```

`nb_log`不仅日志有极其绚烂的各种色彩,`print`也自动有色彩,色彩绚烂远超`loguru`。   
传统 `logging` 无论什么级别日志都是暗红色     
`loguru` 稍微区分了日志级别,对日志级别字段,有各种不同的前景色   
`nb_log` 对各种日志级别和print,采用了背景色 + 前景色渲染,色彩极其夸张,例如 `error`是粉红背景色,`critical`是血红背景色   
**在超高速运行的程序里面,哪怕日志一秒上万条,只要使用`nb_log`,哪怕是800度近视,距离电脑屏幕10米之外,瞟一眼就能知道程序报错没**   


### 1.1.a nb_log 写入日志文件

nb_log默认是只打印到控制台，不会把日志写入到文件、kafka、mongo、es、发邮件和钉钉的，nb_log 记录到每一种地方都有单独的控制参数。

只有get_logger 设置了log_filename，那么该logger才会写到这个文件，日志文件夹的路径是 nb_log_config.py 的 LOG_PATH 配置的。

```python
from nb_log import get_logger
logger = get_logger('logger_namespace',
                    log_filename='namespace_file.log',
                    error_log_filename='f4b_error.log')
logger.debug('这条日志会写到文件中')
```

### 1.1.a2 nb_log 写入日志文件,并将错误日志同时写到另外的错误日志文件中

get_logger 传参了 error_log_filename 后，error级别以上的日志会单独写入到错误文件中。
或者 在nb_log_config.py 配置文件中 配置 AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = True # 自动把错误error级别以上日志写到单独的文件，根据log_filename名字自动生成错误文件日志名字。

```python
from nb_log import get_logger
logger = get_logger('logger_namespace',
                    log_filename='namespace_file.log',
                    error_log_filename='namespace_file_error.log')
logger.debug('这条日志会写到普通文件中')
logger.error('这条日志会写到普通文件中，同时会单独写入到错误文件中')
```

### 1.1.b nb_log 的最核心函数 get_logger入参说明

```doctest
   :param name 日志命名空间，这个是最重要最难理解的一个入参，很多pythoner到现在还不知道name是什么作用。日志命名空间，意义非常非常非常重要，有些人到现在还不知道 logging.getLogger() 第一个入参的作用，太low了。不同的name的logger可以表现出不同的行为。
                例如让 aa命名空间的日志打印控制台并且写入到文件，并且只记录info级别以上，让 bb 命名空间的日志仅仅打印控制台，并且打印debug以上级别，
                这种就可以通过不同的日志命名空间做到。
        :param log_level_int: 日志输出级别，设置为 1 2 3 4 5，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，现在可以直接用10 20 30 40 50了，兼容了。
       :param is_add_stream_handler: 是否打印日志到控制台
       :param is_use_loguru_stream_handler  是否使用 loguru的控制台打印，如果为None，使用 nb_log_config.py的DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER 值。
       :param do_not_use_color_handler :是否禁止使用color彩色日志
       :param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
              非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
       :param log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
       :param error_log_filename :错误日志文件名字，如果文件名不为None，那么error级别以上日志自动写入到这个错误文件。
       :param log_file_size :日志大小，单位M，默认100M
       :param log_file_handler_type :这个值可以设置为1 2 3 4 5 6 7，1为使用多进程安全按日志文件大小切割的文件日志
              2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
              3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
              4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
              5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
                这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
              6 为作者发明的高性能多进程安全，同时按大小和时间切割的文件日志handler
              7 为 loguru的 文件日志记录器
       :param mongo_url : mongodb的连接，为None时候不添加mongohandler
       :param is_add_elastic_handler: 是否记录到es中。
       :param is_add_kafka_handler: 日志是否发布到kafka。
       :param ding_talk_token:钉钉机器人token
       :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
       :param mail_handler_config : 邮件配置
       :param is_add_mail_handler :是否发邮件
       :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                                1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                                如果为logging.Formatter对象，则直接使用用户传入的模板。
       :type log_level_int :int
       :type is_add_stream_handler :bool
       :type log_path :str
       :type log_filename :str
       :type mongo_url :str
       :type log_file_size :int
 
   
```

log_filename 用于设置是否写入日志文件和写入什么文件中。有的人不看入参文档，就问nb_log为什么不写入日志文件中。
logger和handler是观察者模式，日志记录到哪些地方，是由添加了什么handlers决定的。

### 1.1.c nb_log配置文件的生成和导入。

项目中任意脚本使用nb_log,第一次运行代码时候，会自动在 sys.path[1] 目录下创建 nb_log_config.py文件并写入默认值。
之后nb_log 会自动 import nb_log_config, 如果import到这个模块了，控制台会提示读取了什么文件作为配置文件。

如果是 cmd或者linux运行不是pycharm，需要 设置 PYTHONPATH为项目根目录，这样就能自动在当前项目根目录下生成或者找到 nb_log_config.py了。

用户可以print(sys.path)  print(sys.path[1]) 来查看 sys.path[1]的值是什么就知道了。

连PYTHONPATH作用是什么都不知道的python小白，一定要看下面文章 。

[pythonpath作用介绍的文章](https://github.com/ydf0509/pythonpathdemo)


### 1.1.d nb_log_config.py 配置文件的参数说明。

用户可以自己按需修改nb_log_config.py里面的值。

`nb_log_config.py`   
```python

# coding=utf8
"""
此文件nb_log_config.py是自动生成到python项目的根目录的,因为是自动生成到 sys.path[1]。
在这里面写的变量会覆盖此文件nb_log_config_default中的值。对nb_log包进行默认的配置。用户是无需修改nb_log安装包位置里面的配置文件的。

但最终配置方式是由get_logger_and_add_handlers方法的各种传参决定，如果方法相应的传参为None则使用这里面的配置。
"""

"""
如果反对日志有各种彩色，可以设置 DEFAULUT_USE_COLOR_HANDLER = False
如果反对日志有块状背景彩色，可以设置 DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
如果想屏蔽nb_log包对怎么设置pycahrm的颜色的提示，可以设置 WARNING_PYCHARM_COLOR_SETINGS = False
如果想改变日志模板，可以设置 FORMATTER_KIND 参数，只带了7种模板，可以自定义添加喜欢的模板
LOG_PATH 配置文件日志的保存路径的文件夹。
"""
import sys
# noinspection PyUnresolvedReferences
import logging
import os
# noinspection PyUnresolvedReferences
from pathlib import Path  # noqa
import socket
from pythonjsonlogger.jsonlogger import JsonFormatter

# PRINT_WRTIE_FILE_NAME 是 黑科技配置,远超一般日志包所需要管辖的范畴,是nb_log 独门绝技.
# 项目中的print是否自动写入到文件中。值为None则不重定向print到文件中。 自动每天一个文件， 2023-06-30.my_proj.print,生成的文件位置在定义的LOG_PATH
# 如果你设置了环境变量，export PRINT_WRTIE_FILE_NAME="my_proj.print" (linux临时环境变量语法，windows语法自己百度这里不举例),那就优先使用环境变量中设置的文件名字，而不是nb_log_config.py中设置的名字
PRINT_WRTIE_FILE_NAME = os.environ.get("PRINT_WRTIE_FILE_NAME") or Path(sys.path[1]).name + '.print'

# SYS_STD_FILE_NAME 是 黑科技配置,远超一般日志包所需要管辖的范畴,是nb_log 独门绝技.
# 项目中的所有标准输出（不仅包括print，还包括了streamHandler日志）都写入到这个文件，为None将不把标准输出重定向到文件。自动每天一个文件， 2023-06-30.my_proj.std,生成的文件位置在定义的LOG_PATH
# 如果你设置了环境变量，export SYS_STD_FILE_NAME="my_proj.std"  (linux临时环境变量语法，windows语法自己百度这里不举例),那就优先使用环境变量中设置的文件名字，，而不是nb_log_config.py中设置的名字
# 这个相当于是 nohup 自动重定向所有屏幕输出流到一个nohup.out文件的功能了,这个是nb_log日志包的独有黑科技功能,logging 和loguru没这种功能.
# 相对如不同命名空间的logger写入到十几个不同的日志文件,这个SYS_STD_FILE_NAME把项目的所有日志单独重新汇总在一个文件.
SYS_STD_FILE_NAME = os.environ.get("SYS_STD_FILE_NAME") or Path(sys.path[1]).name + '.std'

USE_BULK_STDOUT_ON_WINDOWS = False  # 在win上是否每隔0.1秒批量stdout,win的io太差了

DEFAULUT_USE_COLOR_HANDLER = True  # 是否默认使用有彩的日志。
DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = False  # 是否默认使用 loguru的控制台日志，而非是nb_log的ColorHandler
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True  # 在控制台是否显示彩色块状的日志。为False则不使用大块的背景颜色。
AUTO_PATCH_PRINT = True  # 是否自动打print的猴子补丁，如果打了猴子补丁，print自动变色和可点击跳转。

# 以下是屏蔽控制台所谓的烦人提示项,如果要关闭,先了解下这三个提示是什么,有的pythoner又菜又爱屏蔽提示,然后不知道为什么,这样的人太烦人了.
SHOW_PYCHARM_COLOR_SETINGS = True  # 有的人很反感启动代码时候提示教你怎么优化pycahrm控制台颜色，可以把这里设置为False  (怕提示颜色设置打扰你又不懂pycharm和python的颜色原理,就别抱怨颜色瞎眼)
SHOW_NB_LOG_LOGO = True  # 有的人反感启动代码时候打印nb_log 的logo图形,可以设置为False
SHOW_IMPORT_NB_LOG_CONFIG_PATH = True  # 是否打印读取的nb_log_config.py的文件位置.不懂pythonpath,不懂python导入模块机制的人,别屏蔽了,学习下  https://github.com/ydf0509/pythonpathdemo

WHITE_COLOR_CODE = 37  # 不同pycharm版本和主题,有的对白颜色生效的代号是97,有的是37, 这里可以设置 37和97, 如2023 pycahrm的console color,白颜色捕获的是97,如果这里写37,调节pycharm颜色没法调.

DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER = False  # 是否默认同时将日志记录到记log文件记事本中，就是用户不指定 log_filename的值，会自动写入日志命名空间.log文件中。
AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = False  # 自动把错误error级别以上日志写到单独的文件，根据log_filename名字自动生成错误文件日志名字。
LOG_FILE_SIZE = 1000  # 单位是M,每个文件的切片大小，超过多少后就自动切割
LOG_FILE_BACKUP_COUNT = 10  # 对同一个日志文件，默认最多备份几个文件，超过就删除了。

LOG_PATH = os.getenv("LOG_PATH")  # 优先从环境变量获取,启动代码之前可以 export LOG_PATH = '/你的日志目录/'
if not LOG_PATH:
    LOG_PATH = '/pythonlogs'  # 默认的日志文件夹,如果不写明磁盘名，则是项目代码所在磁盘的根目录下的/pythonlogs
    # LOG_PATH = Path(__file__).absolute().parent / Path("pythonlogs")   #这么配置就会自动在你项目的根目录下创建pythonlogs文件夹了并写入。
    if os.name == 'posix':  # linux非root用户和mac用户无法操作 /pythonlogs 文件夹，没有权限，默认修改为   home/[username]  下面了。例如你的linux用户名是  xiaomin，那么默认会创建并在 /home/xiaomin/pythonlogs文件夹下写入日志文件。
        home_path = os.environ.get("HOME", '/')  # 这个是获取linux系统的当前用户的主目录，不需要亲自设置
        LOG_PATH = Path(home_path) / Path('pythonlogs')  # linux mac 权限很严格，非root权限不能在/pythonlogs写入，修改一下默认值。
# print('LOG_PATH:',LOG_PATH)

LOG_FILE_HANDLER_TYPE = 6  # 1 2 3 4 5 6 7   # nb_log 的日志切割,全都追求多进程下切割正常.
"""
LOG_FILE_HANDLER_TYPE 这个值可以设置为 1 2 3 4 5 四种值，
1为使用多进程安全按日志文件大小切割的文件日志,这是本人实现的批量写入日志，减少操作文件锁次数，测试10进程快速写入文件，win上性能比第5种提高了100倍，linux提升5倍
2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个新的日志文件。日志文件名字后缀自动加上日期。
3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题) 
4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
   这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
6 BothDayAndSizeRotatingFileHandler 使用本人完全彻底开发的，同时按照时间和大小切割，无论是文件的大小、还是时间达到了需要切割的条件就切割。
7 LoguruFileHandler ,使用知名的 loguru 包的文件日志记录器来写文件。
"""

LOG_LEVEL_FILTER = logging.DEBUG  # nb_log.get_logger不指定日志级别时候，默认日志级别，低于此级别的日志不记录了。例如设置为INFO，那么logger.debug的不会记录，只会记录logger.info以上级别的。
# 强烈不建议调高这里的级别为INFO，日志是有命名空间的，单独提高打印啰嗦的日志命名空间的日志级别就可以了，不要全局提高日志级别。
# https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c9.html#id2  文档9.5里面讲了几百次 python logging的命名空间的作用了，有些人到现在还不知道日志的name作用。

ROOT_LOGGER_LEVEL = logging.INFO # 根日志命名空间的日志级别，如果是INFO，没有添加handlers的其他命名空间的日志info及以上级别都会被记录，你可以亲自设置日志级别。
ROOT_LOGGER_FILENAME ='root.log' # 根日志命名空间的日志文件名字，默认是root.log。可以设置为None,则不记录到文件中。
ROOT_LOGGER_FILENAME_ERROR = 'root.error.log'  #  # 根日志命名空间的error级别以以上的日志单独文件名字。可以设置为None,则不另外生成一个error日志文件。

# 屏蔽的字符串显示，用 if in {打印信息} 来判断实现的,如果打印的消息中包括 FILTER_WORDS_PRINT 数组中的任何一个字符串，那么消息就不执行打印。
# 这个配置对 print 和 logger的控制台输出都生效。这个可以过滤某些啰嗦的print信息，也可以过滤同级别日志中的某些烦人的日志。可以用来过滤三方包中某些控制台打印。数组不要配置过多，否则有一丝丝影响性能会。
FILTER_WORDS_PRINT = []  # 例如， 你希望消息中包括阿弥陀佛 或者 包括善哉善哉 就不打印，那么可以设置  FILTER_WORDS_PRINT = ['阿弥陀佛','善哉善哉']


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
        log_record[f"{record.__dict__.get('pathname')}:{record.__dict__.get('lineno')}"] = ''  # 加个能点击跳转的字段。
        log_record['ip'] = computer_ip
        log_record['host_name'] = computer_name
        super().add_fields(log_record, record, message_dict)
        if 'for_segmentation_color' in log_record:
            del log_record['for_segmentation_color']


DING_TALK_TOKEN = '3dd0eexxxxxadab014bd604XXXXXXXXXXXX'  # 钉钉报警机器人

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
        '日志时间【%(asctime)s】 - 日志名称【%(name)s】 - 文件【%(filename)s】 - 第【%(lineno)d】行 - 日志等级【%(levelname)s】 - 日志信息【%(message)s】',
        "%Y-%m-%d %H:%M:%S"),
    2: logging.Formatter(
        '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),
    3: logging.Formatter(
        '%(asctime)s - %(name)s - 【 File "%(pathname)s", line %(lineno)d, in %(funcName)s 】 - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 一个模仿traceback异常的可跳转到打印日志地方的模板
    4: logging.Formatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
        "%Y-%m-%d %H:%M:%S"),  # 这个也支持日志跳转
    5: logging.Formatter(
        '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 我认为的最好的模板,推荐
    6: logging.Formatter('%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
                         "%Y-%m-%d %H:%M:%S"),
    7: logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # 一个只显示简短文件名和所处行数的日志模板

    8: JsonFormatterJumpAble('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s %(lineno)d  %(process)d %(thread)d', "%Y-%m-%d %H:%M:%S.%f",
                             json_ensure_ascii=False),  # 这个是json日志，方便elk采集分析.

    9: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 对5改进，带进程和线程显示的日志模板。
    10: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # 对7改进，带进程和线程显示的日志模板。
    11: logging.Formatter(
        f'%(asctime)s-({computer_ip},{computer_name})-[p%(process)d_t%(thread)d] - %(name)s - "%(filename)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # 对7改进，带进程和线程显示的日志模板以及ip和主机名。
}

FORMATTER_KIND = 5  # 如果get_logger不指定日志模板，则默认选择第几个模板

```

以上只是部分配置的例子，其他配置在你项目根目录下的 nb_log_config.py中都有默认值，自己按需修改设置。
其他例如日志模板定义，默认日志模板选择什么，都可以在 nb_log_config.py文件中设置。


### 1.1.1e  日志配置文件和get_logger传参的关系。


nb_log_config.py中是设置全局设置，get_logger是针对单个logger对象生成的设置。

例如 nb_log_config.py 中写 FORMATTER_KIND = 4，get_logger 传参 formatter_template=6，那么最终还是使用第6个日志模板。
如果get_logger函数没有传参指定就使用 nb_log_config.py中的配置。
就是说 get_logger 是优先级高的，nb_log_config.py 是优先级低的配置方式。



## 1.2 nb_log功能介绍

### 1.2.1 nb_log 支持日志根据级别自动变彩色

如图：日志彩色符合交通灯颜色认知。绿色是debug等级的日志，天蓝色是info等级日志，
黄色是warnning等级的警告日志，粉红色是error等级的错误日志，血红色是criticl等级的严重错误日志

### 1.2.1b 设置是否需要彩色
nb_log支持自动彩色，也支持关闭背景色块只要颜色，也支持彻底不要颜色所有日志显示为正常黑白颜色。

可以在你项目根目录下自动生成的nb_log_config.py配置文件中修改相关配置，来控制是否需要颜色，或者要颜色但不要大块的背景色块。

```angular2html
如果反对日志有各种彩色，可以设置 DEFAULUT_USE_COLOR_HANDLER = False
如果反对日志有块状背景彩色，可以设置 DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
如果想屏蔽nb_log包对怎么设置pycahrm的颜色的提示，可以设置 WARNING_PYCHARM_COLOR_SETINGS = False
如果想改变日志模板，可以设置 FORMATTER_KIND 参数，只带了7种模板，可以自定义添加喜欢的模板
LOG_PATH 配置文件日志的保存路径的文件夹。
```

### 1.2.1c 关于彩色显示效果的最终显示的说明

有的人听说了python显示颜色的博客，例如这种

[python print显示颜色](https://www.cnblogs.com/ping-y/p/5897018.html)

```
python在控制台可以同时显示7种颜色，但是同时显示不出来65536种颜色，pycahrm控制台/win cmd/linux的控制台终端不是浏览器网页，不能显示丰富的65536色模式，
只能暴露7种ansi颜色钩子，显示控制台输出的终端软件一般提供了颜色的自定义设置，例如 pycahrm finashell xhsell
这些软件都可以对ansi颜色自定义65536色模式的颜色代码，
例如nb_log启动时候就打印提示了教用户怎么设置颜色。

例如一件拍摄街道的彩色相片有60多种颜色，在cmd pycahrm终端是不可能同时显示出那么多种颜色的。
例如你想要控制台显示杨幂穿的淡红色衣服的颜色，控制台能做得到吗？当然是能做到得，但不是在python种 用所谓得  \033[ 来设置颜色，
因为软件终端只能识别7种ansi颜色钩子，红色在65536色模式下最起码也有几万种颜色代码，有白浅红色 水红色 大红色 粉红色 红的发紫的红色 红得发黑的红色，
所以你想精确得让控制台显示多种不同的红色，你自己用大脑想想呗，仅仅在python print中 \033就想得到理想的所需的红色，简直是做梦吧。
我说的是要精确控制颜色，不能光靠python的\033[，而是要在python的终端输出软件中设置颜色。例如pycharm xhsell finashell软件中都支持自定义颜色。

所以有些小白用户觉得颜色不好看，让我在配置文件中放开自定义颜色，这是不可行的，颜色最终的显示效果由控制台终端决定，不是所谓的\033能决定的，
例如我就想问  \033后面加什么字母能精确得到桃红色 金黄色 亮绿色这些 ，这么简单的想不到吗？如果控制台自动支持65536种颜色同时显示，那么nb_log可以暴露出来怎么配置颜色。
例如  \033[32  是绿色，但是软件终端中重定义ansi 颜色，可以让你代码的\033[32 显示出1万种不同的绿色，当然也可以让\033[32 绿色但是显示成黄色 紫色啥的，
因为最终渲染颜色效果是由终端决定，不是代码中\033后面数字来决定的。用户需要在软件终端中重新定义颜色，拿pycahrm为例，设置各种想要的颜色30秒钟，配置颜色要不了很久。

```

### 1.2.1d pycharm中精确设置控制台颜色的方式
```
要说明的是，即使是同一个颜色代码在pycahrm不同主题都是颜色显示区别很大的，默认的可能很丑或者由于颜色不好导致文字看不清晰
为了达到我这种色彩效果需要重新设置主题颜色，在控制台输出的第一行就教大家怎么设置颜色了。
也可以按下面设置，需要花30秒设置。


1)使用pycharm时候，建议重新自定义设置pycharm的console里面的主题颜色。
设置方式为 打开pycharm的 file -> settings -> Editor -> Color Scheme -> Console Colors 选择monokai，
并重新修改自定义7个颜色，设置Blue为 0454F3 ，Cyan为 04DCF8 ，Green 为 13FC02 ，Magenta为 ff1cd5 ,red为 F80606 ，yellow为 EAFA04 ，gray 为 FFFFFF ，white 为 FFFFFF 。
如果设置为显示背景色快，由于不同版本的pycahrm或主题，可以根据控制台实际显示设置 White 为 1F1F1F， Black 为 FFFFFF，因为背景色是深色，前景色的文字设置为白色比黑色好。

2)使用xshell或finashell工具连接linux也可以自定义主题颜色，默认使用shell连接工具的颜色也可以。

```

### 1.2.2 nb_log 不仅支持日志变彩色，还支持项目中所有python文件的任意print自动变彩色

```
导入nb_log时候会给内置的 ptint 打猴子补丁，所以用户所有地方的print行为自动发生了变化，重定向到nb_log定义的print了
```

### 1.2.2b print自动化效果转换的好处说明
```
自动转换print效果，再也不怕有人在项目中随意print，导致很难找到是从哪里冒出来的print。
只要import nb_log，项目所有地方的print自动现型并在控制台可点击几精确跳转到print的地方。

在项目里面的几百个文件中疯狂print真的让人很生气，一个run.py运行起来几百个py文件，
每个文件print 七八次，到底自己想看想关心的print是在控制台的哪一行呢，找到老眼昏花都找不到。
比如打印x变量的值，有人是为了省代码直接 print(x)，而没有多打几个字母使用print("x的值是：",x)，
这样打印出来的x变量，根本无法通过全局查找找到打印x变量是在什么py文件的哪一行。

有人说把之前的print全部用#注释不就好了，那这要全局找找print，一个一个的修改，一个10万行项目， 
就算平均100行有一个print关键字，那起码也得有1000个print关键字吧，一个个的修改那要改到猴年马月呢。

只有使用nb_log，才能让一切print妖魔鬼怪自动现形。

另外，在正式项目或工具类甚至做得包里面，疯狂print真的很low，可以参考大神的三方包，从来都没直接print的不存在的，
他们都是用的日志。
日志比print灵活多了，对命名空间的控制、级别过滤控制、模板自定义、能记录到的地方扩展性很强远强过print的只有控制台。
```

### 1.2.2c nb_log 五彩日志的效果截图


[![pkFSO3V.png](https://s21.ax1x.com/2024/04/29/pkFSO3V.png)](https://imgse.com/i/pkFSO3V)


## 1.3 nb_log 支持pycharm控制台点击日志精确跳转到打印日志的文件和行号

[![8tka3.png](https://i.postimg.cc/GhRFq5H9/8tka3.png)](https://postimg.cc/w3WRBF5d)

## 1.4 nb_log是原生logging类型，兼容性 扩展性非常好。

nb_log 是基于python自带的原生logging模块封装的， nb_log.get_logger()生成的日志类型是 原生logging.Logger类型，
所以nb_log包对常用三方包日志兼容性替换芯做到了100%。是否是原生日志非常重要，logbook和loguru都不是python自带的原生日志，
所以和三方包结合或者替换性不好。

```
比如logru和logbook这种三方库，完全重新写的日志，
它里面主要被用户使用的logger变量类型不是python内置Logger类型，
造成logger说拥有的属性和方法有的不存在或者不一致，这样的日志和python内置的经典日志兼容性差，
只能兼容（一键替换logger类型）一些简单的debug info warning errror等方法，。
```

## 1.5 nb_log 能够简单讲日志记录到十几种地方的任意几种的组合。


内置了一键入参，每个参数是独立开关，可以把日志同时记录到10几个常用的地方的任意几种组合，
包括 控制台 文件 钉钉 邮件 mongo kafka es 等等 。

有的人以为日志只能记录到控制台和文件，其实是错的，日志可以记录到很多种地方，日志记录到哪里，是由logger添加了什么handler决定的。


## 1.6 日志命名空间独立，采用了多实例logger，按日志命名空间区分。

```python
"""
命名空间独立意味着每个logger单独的日志界别过滤，单独的控制要记录到哪些地方。
"""

from nb_log import get_logger, LogManager

logger_aa = LogManager('aa').get_logger_and_add_handlers(10, log_filename='aa.log')
logger_bb = get_logger("bb", log_level_int=30, is_add_stream_handler=False, ding_talk_token='your_dingding_token')
logger_cc = get_logger('cc', log_level_int=10, log_filename='cc.log')

logger_aa.debug('哈哈哈')
# 将会同时记录到控制台和文件aa.log中，只要debug及debug以上级别都会记录。

logger_bb.warning('嘿嘿嘿')
# 将只会发送到钉钉群消息，并且logger_bb的info debug级别日志不会被记录，非常方便测试调试然后稳定了调高界别到生产。

logger_cc.debug('嘻嘻')
# logger_cc的日志会写在cc.log中，和logger_aa的日志是不同的文件。
```

python命名空间非常重要,有的人太笨了,说设置了级别为logging.WARN,但是debug还是被记录,就是因为他牛头不对马嘴,忽视了是对什么命名空间设置的日志级别,debug日志又是什么命名空间的日志打印出来的

搜索一下文档的"命名空间"4个字,文档里面谈了几百次这个概念了,有的人logging基础太差了,令人吐血,需要在nb_log文档来讲,这样导致nb_log文档很长.



## 1.7 对内置looging包打了猴子补丁，使日志永远不会使用同种handler重复记录 ，例如，原生的

```
from logging import getLogger,StreamHandler
logger = getLogger('hi')
getLogger('hi').addHandler(StreamHandler())
getLogger('hi').addHandler(StreamHandler())
getLogger('hi').addHandler(StreamHandler())
logger.warning('啦啦啦')

明明只warning了一次，但实际会造成 啦啦啦 在控制台打印3次。
使用nb_log，对同一命名空间的日志，可以无惧反复添加同类型handler，不会重复记录。

关于重复记录的例子，更惨的例子在文档后面的例子，直接把机器cpu性能耗尽，磁盘弄爆炸。
```

## 1.8 nb_log使用对比原生logging和 loguru 更简单

### 1.8.1 logging 代码方式创建logger对象

```python
import logging
logger = logging.getLogger('my.logger.namespace')

fh = logging.FileHandler('test.log')  # 可以向文件发送日志

ch = logging.StreamHandler()  # 可以向屏幕发送日志

fm = logging.Formatter('%(asctime)s %(message)s')  # 打印格式

fh.setFormatter(fm)
ch.setFormatter(fm)

logger.addHandler(fh)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)  # 设置级别


logger.debug('debug 喜喜')

```

有些人简直是怕了原生logging了，为了创建一个好用的logger对象，代码步骤复杂的吓人，很多人完全没看懂这段代码意义，
因为他是一步步创建观察者handler，给handler设置好看的formattor，给给被观察者添加多个观察者对象。
大部分人不看设计模式，不仅不懂观察者模式，而且没听说观察者模式，所以这种创建logger方式完全蒙蔽的节奏。
其实这样一步步的写代码是为了给用户最大的自由来怎么创建一个所需的logger对象。如果高度封装创建logger过程那是简单了，
但是自定义自由度就下降了。
logging是原生日志，每个三方包肯定使用logging了，为了兼容性和看懂三方包，那肯定是要学习logging的，对logging望而却步，
想投机取巧只使用loguru是行不通的，三方包不会使用loguru，三方包里面各种命名空间的日志，等待用户添加handlers来记录日志，
loguru缺点太大了。

nb_log把logging创建logger封装了，但同时get_logger暴露了很多个入参，来让用户自由自定义logger添加什么handler和设置什么formattor。
所以nb_log有原生logging的普遍兼容性，又使用简单


### 1.8.2 python中 创建logger的第二种方式，logging.config.dictConfig()

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
 
# 运行测试
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("console_logger")
logger.debug('debug message')
logger.info('info message')
logger.warn('warning message')
logger.error('error message')
logger.critical('critical message')


```

这种方式和上面1.8.1的方式差不多, 但不需要写大量python代码来创建logger对象。
虽然不需要写大量python代码来构建logger对象，但是需要写 LOGGING_CONFIG 字典，
这种字典如果写错了导致配置不生效或者报错，还是很麻烦的。很多人对这个配置完全蒙蔽，不知道什么意思。

先创建formattor，创建文件和控制台handler(当然也可以自定义发送钉钉的handler)，handler设置日志过滤级别，handler设置formattor，
不同的handler可以设置不同的formattor，例如同样是 logger.debug("hello world"),可以使文件和控制台记录的这条日志的前缀和字段不一样。

对不同命名空间的logger添加不同的handlers，
例如你只想打印控制台 就 logger = logging.getLogger("console_logger")，然后用这个logger.info(xxx)就可以打印控制台了。
例如你只想打写入文件 就 logger = logging.getLogger("file_logger")，然后用这个logger.info(xxx)就可以打印控制台了。
例如你打写入文件并且打印控制台 就 logger = logging.getLogger("console_plain_file_logger")，然后用这个logger.info(xxx)就可以打印控制台并且同时写入文件了。


对1.8.1和1.8.2不理解造成恐惧，是使大家使用loguru的主要原因。


### 1.8.3 loguru的简单使用

```python
from loguru import logger
logger.add("./log_files/loguru-test1.log",  rotation="100000 KB")
logger.info("hello")
```

```
代码是loguru打印控制台和写入文件，和nb_log一样代码少。
甚至如果用户不需要写入文件只需要导入logger就好了，

from loguru import logger
logger.info("hello")

看起来很简单，nb_log还需要 get_logger一下，有的人觉得loguru少写一行代码，直接import就能使用了，所以loguru简单牛逼。
nb_log早就知道有人会这么想了，nb_log也支持导入即可使用。

from nb_log import defaul_logger
defaul_logger.info("hello")

但这样有个弊端，用户想使用什么日志模板，用户希望日志记录到 控制台 文件 钉钉 es中的哪几个地方没法定义。
用户如果想屏蔽a函数里面的日志，但想放开b函数里面的日志，这种不传参/不设置日志命名空间的日志就无能为力做到了。
所以nb_log推荐用户调用get_logger函数来自定义日志，而不是直接import defaul_logger然后所有地方都使用这个 defaul_logger来记录日志。
```

### 1.8.4 nb_log的使用可以比loguru更简单

loguru:
```
from loguru import logger
logger.add("./log_files/loguru-test1.log",  rotation="100000 KB")
logger.info("hello")
```

nb_log ,你想简单不想get_loger,你想粗暴的导入就能记录日志到控制台和文件，代码如下：
```
import nb_log

nb_log.debug('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用debug函数，那就满足这种人')
nb_log.info('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用info函数，那就满足这种人')
nb_log.warning('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用warning函数，那就满足这种人')
nb_log.error('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用error函数，那就满足这种人')
nb_log.critical('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用critical函数，那就满足这种人')

```

[![pPSPUDs.png](https://s1.ax1x.com/2023/07/28/pPSPUDs.png)](https://imgse.com/i/pPSPUDs)

```
有的笨瓜总是不能理解 logging.getLogger第一个入参name的作用和巨大好处，老是觉得需要实例化生成 logger 对象觉得麻烦，想开箱即用，那就满足这种人。
用from loguru import logger 这种日志，先不同模块或功能的日志设置不同级别，不同的模块写入不同的文件，非常麻烦不优雅。
但有的人完全不理解 日志命名空间的作用，只会抱怨nb_log的例子要他实例化不同name的logger麻烦，那就满足这种人，不用他手动实例化生成不同命名空间的logger。

import nb_log

nb_log.debug('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用debug函数，那就满足这种人')
nb_log.info('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用info函数，那就满足这种人')
nb_log.warning('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用warning函数，那就满足这种人')
nb_log.error('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用error函数，那就满足这种人')
nb_log.critical('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用critical函数，那就满足这种人')


loguru的用法是：
from loguru import logger
logger.debug(msg)

nb_log的用法是：
import nb_log
nb_log.debug(msg)

nb_log比loguru少了 from import那不是更简洁了吗？满足这种只知道追求简单的笨瓜。
```



综上所述 nb_log既使用简单，又兼容性高。

## 1.9 内置logging包的日志命名空间是什么

```python
import logging
logger1 = logging.getLogger('aaa')

logger2 = logging.getLogger('aaa')

logger3 = logging.getLogger('bbb')

print('logger1 id: ',id(logger1),'logger2 id: ',id(logger2),'logger3 id: ',id(logger3))
```

运行上面可以发现 logger1和logger2对象是同一个id，logger3对象是另外一个id。
通过不同的日志命名空间，可以设置不同级别的日志显示，设置不同类型的日志记录到不同的文件，是否打印控制台，是否发送邮件 钉钉消息。

<pre style="font-size: large;color: #FFFF66;background-color: #0c1119">
有的人到现在还是不知道日志命名空间的作用，对一个大项目的所有的日志只会处理成一种表现行为，悲了个剧。
如果有人说某部分的日志打印啰嗦了，会说把日志级别调高，这是很外行的说法，请问你如何调高日志级别？有的人不懂日志命名空间，那是完全无法调日志界别，
比如1.9中的代码，有的笨瓜把 logger3的 logger3.s

你把日志界别调高了，另一个模块或类或函数里面的日志你希望需要显示debug日志呢，
你只是要屏蔽某些debug日志，
</pre>

### 1.9.2 看大神和小白是怎么记录flask的请求记录和报错记录的,为什么知道日志 logger 的name 很重要?

#### 1.9.2.a  小白记录flask日志,不知道日志命名空间,脱裤子放屁手写记录日志做无用功
```python
"""
1) 在接口中自己去手写记录请求入参和url,脱裤子放屁
2) 在接口中手写记录flask接口函数报错信息

就算你在框架层面去加日志或者接口加装饰器记录日志,来解决每个接口重复写怎么记录日志,那也是很low,

不懂日志命名空间就重复做无用功,这些记录人家框架早就帮你记录了,只是没加日志 handler,等待用户来加而已
"""
import traceback
from flask import Flask, request
from loguru import logger

app = Flask(__name__)

logger.add('mylog.log')


@app.route('/')
def hello():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr) # 写这行拖了裤子放屁
    return 'Hello World!'


@app.route('/api2')
def api2():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr)
    try:
        1 / 0  # 故意1/0 报错
        return '2222'
    except Exception as e:
        logger.error(f'e {traceback.format_exc()}')  # 写这行拖了裤子放屁


if __name__ == '__main__':
    app.run()

```

#### 1.9.2.b  知道日志命名空间的大神记录flask日志,完全不需要手写记录日志
```python
"""
这个代码里面没有手写任何怎么记录flask的请求和flask异常到日志,但是可以自动记录.
这就是大神玩日志,懂命名空间.

这才是正解, werkzeug 命名空间加上各种handler,
只要请求接口,就可以记录日志到控制台和文件werkzeug.log了,

这里的flask的app的name写的是myapp ,flask框架生成的日志命名空间复用app.name,
所以给myapp加上handler,那么flask接口函数报错,就可以自动记录堆栈报错到 myapp.log 和控制台了.

"""

from flask import Flask, request
import nb_log

app = Flask('myapp')

nb_log.get_logger('werkzeug', log_filename='werkzeug.log')

nb_log.get_logger('myapp', log_filename='myapp.log')


@app.route('/')
def hello():
    # 接口中无需写日志记录请求了什么url和入参
    return 'Hello World!'


@app.route('/api2')
def api2():
    # 接口中无需写日志记录报什么错了
    1 / 0
    return '2222'


if __name__ == '__main__':
    app.run(port=5002)
```

```
从上面的对比可以看出,不懂日志命名空间有多么low,天天做无用功记录日志
```

有人问我是怎么知道要记录 werkzeug 和 myapp 这两个日志命名空间的日志?

```
这个不是我耍赖先百度了,然后才知道要记录 werkzeug,完全不需要耍赖

nb_log.get_logger(name=None) 可以记录任意三方包模块的一切日志命名空间的日志,
先让name=None,由于控制台的模板加了name字段,所以可以看到是什么命名空间打印的日志,然后就知道要记录哪些命名空间的日志了.
```

## 1.10 nb_log比logurur有10胜

[nb_log比logurur有10个优点方面](https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c6.html)


## 1.10.b nb_log 新增支持loguru包来记录日志，原汁原味的loguru

get_logger 传参 is_use_loguru_stream_handler=True 或者 nb_log_config.py 设置 DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = True，那么就是使用loguru来打印控制台。

get_logger 传参 log_file_handler_type=7 或者 nb_log_config.py 设置 LOG_FILE_HANDLER_TYPE = 7，那么就使用loguru的文件日志handler来写文件。


通过nb_log操作logurur很容易实现 a函数的功能写入a文件，b函数的功能写入b文件。

代码如下：

```python
import time

import nb_log

logger = nb_log.get_logger('name1', is_use_loguru_stream_handler=True, log_filename='testloguru_file111.log',log_file_handler_type=7)
logger2 = nb_log.get_logger('name2', is_use_loguru_stream_handler=True, log_filename='testloguru_file222.log',log_file_handler_type=7)

for i in range(10000000000):
    logger.debug(f'loguru debug 111111')
    logger2.debug(f'loguru debug 222222')

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

# 通过这样,给相应命名空间加上loguru的handler,使loguru能自动记录django flask requests urllib3的logging日志,
# 直接使用loguru来记录三方库的日志很难,但使用nb_log的loguru模式来实现记录第三方库的logging日志,却非常简单.
nb_log.get_logger('urllib3', is_use_loguru_stream_handler=True)

requests.get('http://www.baidu.com')  


time.sleep(100000)
```

之前有人还是质疑怀疑nb_log不如loguru，现在nb_log完全支持了 loguru，那还有什么要质疑的。

就如同有人怀疑funboost框架，那么funboost就增加支持celery整体作为broker，完全使用celery的调度核心来执行函数，还比亲自操作celery简单很多。

作者一直是包容三方框架的，说服不了你，就兼容第三方包。

## 1.11 关于nb_log日志级别设置，看文档9.5 章节。

要精通python logging.getLogger第一个入参意义，非常非常重要。

[关于nb_log日志级别设置](https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c9.html#id2)

## 1.20 完整readthedocs文档地址

[nb_log readthedocs文档链接](https://nb-log-doc.readthedocs.io/zh_CN/latest)

[nb_log 源码链接](https://github.com/ydf0509/nb_log)

![](https://visitor-badge.glitch.me/badge?page_id=nb_log)

<div> </div>

`````

--- **end of file: source/articles/c1.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c10.md** (project: nb_log) --- 

`````markdown
# 10 nb_log 更新记录

## 10.1 2023.07  nb_log 新增 print和标准输出 自动写入到文件中

按照网友的建议，nb_log 新增 print和标准输出 自动写入到文件中

此功能是通过对print和sys.stdout/stderr打强力的猴子补丁的方式实现的，用户的print和没有添加fileHandler只有streamHandler的日志可以自动写入到文件中。

此项功能可以通过nb_log_config.py 或者环境变量来配置，是否自动写入到文件和写入到什么文件名字。

nb_log_config.py中
```
# 项目中的print是否自动写入到文件中。值为None则不重定向标准输出到文件中。 自动每天一个文件， 2023-06-30.my_proj.out,生成的文件位置在定义的LOG_PATH
# 如果你设置了环境变量，export PRINT_WRTIE_FILE_NAME="my_proj.print" (linux临时环境变量语法，windows语法自己百度这里不举例),那就优先使用环境变量中设置的文件名字，而不是nb_log_config.py中设置的名字
PRINT_WRTIE_FILE_NAME = Path(sys.path[1]).name + '.print' 

# 项目中的所有标准输出（不仅包括print，还包括了streamHandler日志）都写入到这个文件。自动每天一个文件， 2023-06-30.my_proj.std,生成的文件位置在定义的LOG_PATH
# 如果你设置了环境变量，export SYS_STD_FILE_NAME="my_proj.std"  (linux临时环境变量语法，windows语法自己百度这里不举例),那就优先使用环境变量中设置的文件名字，，而不是nb_log_config.py中设置的名字
SYS_STD_FILE_NAME = Path(sys.path[1]).name + '.std'    
```


## 10.2 2023.12 新增 错误error级别以上日志文件写入单独的日志文件中

看文档1.1.a2

## 10.3 2023.12 新增 支持loguru来打印控制台和写入文件

看文档 1.10.b
`````

--- **end of file: source/articles/c10.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c2.md** (project: nb_log) --- 

`````markdown
# 2 nb_log的文件日志handler

## 2.1 nb_log 支持5中文件日志切割方式

这个文件日志的自定义多进程安全按大小切割，filehandler是python史上性能最强大的支持多进程下日志文件按大小自动切割。

关于按大小切割的性能可以看第10章的和loggeru的性能对比，nb_log文件日志写入性能快400%。

nb_log 支持5种文件日志，get_logger 的log_file_handler_type可以优先设置是按照 大小/时间/watchfilehandler/单文件永不切割.

也可以在你代码项目根目录下的 nb_log_config.py 配置文件的 LOG_FILE_HANDLER_TYPE 设置默认的filehandler类型。

nb_log_config.py 的 LOG_PATH 配置默认的日志文件夹位置，如果get_logger函数没有传log_path入参，就默认使用这里的LOG_PATH

```
在各种filehandler实现难度上 
单进程永不切割  < 单进程按大小切割 <  多进程按时间切割 < 多进程按大小切割

因为每天日志大小很难确定，如果每天所有日志文件以及备份加起来超过40g了，硬盘就会满挂了，所以nb_log的文件日志filehandler默认采用的是按大小切割，不使用按时间切割。

文件日志自动使用的默认是多进程安全切割的自定义filehandler，
logging包的RotatingFileHandler多进程运行代码时候，如果要实现向文件写入到规定大小时候并自动备份切割，win和linux都100%报错。

支持多进程安全切片的知名的handler有ConcurrentRotatingFileHandler，
此handler能够确保win和linux切割正确不出错，此包在linux使用的是高效的fcntl文件锁，
在win上性能惨不忍睹，这个包在win的性能在三方包的英文说明注释中，作者已经提到了。

nb_log是基于自动批量聚合，从而减少写入次数（但文件日志的追加最多会有1秒的延迟），从而大幅度减少反复给文件加锁解锁，
使快速大量写入文件日志的性能大幅提高，在保证多进程安全且排列的前提下，对比这个ConcurrentRotatingFileHandler
使win的日志文件写入速度提高100倍，在linux上写入速度提高10倍。

```

## 2.2 演示nb_log文件日志，并且直接演示最高实现难度的多进程安全切片文件日志

```python
from multiprocessing import Process
from nb_log import LogManager, get_logger

# 指定log_filename不为None 就自动写入文件了，并且默认使用的是多进程安全的切割方式的filehandler。
# 默认都添加了控制台日志，如果不想要控制台日志，设置is_add_stream_handler=False
# 为了保持方法入场数量少，具体的切割大小和备份文件个数有默认值，
# 如果需要修改切割大小和文件数量，在当前python项目根目录自动生成的nb_log_config.py文件中指定。

# logger = LogManager('ha').get_logger_and_add_handlers(is_add_stream_handler=True,
# log_filename='ha.log')
# get_logger这个和上面一句一样。但LogManager不只有get_logger_and_add_handlers一个公有方法。
logger = get_logger(is_add_stream_handler=True, log_filename='ha.log')


def f():
    for i in range(1000000000):
        logger.debug('测试文件写入性能，在满足 1.多进程运行 2.按大小自动切割备份 3切割备份瞬间不出错'
                     '这3个条件的前提下，验证这是不是python史上文件写入速度遥遥领先 性能最强的python logging handler')


if __name__ == '__main__':
    [Process(target=f).start() for _ in range(10)]
```

## 2.3 演示文件大小切割在多进程下的错误例子,

```
注意说的是多进程，任何handlers在多线程下都没有问题，任何handlers在记录时候都加了线程锁了，完全不用考虑多线程。
线程锁不能跨进程特别是跨不同批次启动的脚本运行的解释器。
所以说的是多进程，不是多线程。

下面这段代码会疯狂报错。因为每达到100kb就想切割，多个文件句柄引用了同一个文件，某个进程想备份改文件名，别的进程不知情。

解决这种问题，有人会说用进程锁，那是不行的，如果把xx.py分别启动两次，没有共同的父子进程，属于跨解释器的，进程锁是不行的。

nb_log是采用的文件锁，文件锁在linux性能比较好，在win很差劲，导致日志拖累真个代码的性能，所以nb_log是采用把每1秒内的日志
聚合起来，写入一次文件，从而大幅减少了加锁解锁次数，
对比有名的concurrent_log_handler包的ConcurrentRotatingFileHandler，在win上疯狂快速写日志的性能提高了100倍，
在linux上也提高了10倍左右的性能。
```

```python

"""
只要满足3个条件
1.文件日志
2.文件日志按大小或者时间切割
3.多进程写入同一个log文件，可以是代码内部multiprocess.Process启动测试，
  也可以代码内容本身不用多进程但把脚本反复启动运行多个来测试。

把切割大小或者切割时间设置的足够小就很容易频繁必现，平时有的人没发现是由于把日志设置成了1000M切割或者1天切割，
自测时候只随便运行一两下就停了，日志没达到需要切割的临界值，所以不方便观察到切割日志文件的报错。

这里说的是多进程文件日志切割报错即多进程不安全，有的人强奸民意转移话题老说他多线程写日志切割日志很安全，简直是服了。
面试时候把多进程和多线程区别死记硬背 背的一套一套很溜的，结果实际运用连进程和线程都不分。
"""
from logging.handlers import RotatingFileHandler
import logging
from multiprocessing import Process
from threading import Thread

logger = logging.getLogger('test_raotating_filehandler')

logger.addHandler(RotatingFileHandler(filename='testratationg.log', maxBytes=1000 * 100, backupCount=10))


def f():
    while 1:
        logger.warning('这个代码会疯狂报错，因为设置了100Kb就切割并且在多进程下写入同一个日志文件' * 20)


if __name__ == '__main__':
    for _ in range(10):
        Process(target=f).start()  # 反复强调的是 文件日志切割并且多进程写入同一个文件，会疯狂报错
        # Thread(target=f).start()  # 多线程没事，所有日志handler无需考虑多线程是否安全，说的是多进程文件日志切割不安全，你老说多线程干嘛？
```

[![hVT2CV.png](https://z3.ax1x.com/2021/08/25/hVT2CV.png)](https://imgtu.com/i/hVT2CV)



<div> </div>
`````

--- **end of file: source/articles/c2.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c3.md** (project: nb_log) --- 

`````markdown
# 3. nb_log记录到 钉钉、Mongo、elastic、邮件等

## 3.1 钉钉日志

```python
from nb_log import get_logger

logger4 = get_logger("hi", is_add_stream_handler=True,
                     log_filename="hi.log", ding_talk_token='your_dingding_token')
logger4.debug('这条日志会同时出现在控制台 文件 和钉钉群消息')
```

## 3.2 其他handler包括kafka日志，elastic日志，邮件日志，mongodb日志

按照get_logger_and_add_handler函数的入参说明就可以了，和上面的2 3 4中的写法方式差不多，都是一参 傻瓜式，设置了，日志记录就会记载在各种地方。


## 3.3 各種日志截圖

钉钉

<a href="https://imgse.com/i/pkFpk36"><img src="https://s21.ax1x.com/2024/04/29/pkFpk36.png" alt="pkFpk36.png" border="0" /></a>



邮件日志
<a href="https://imgse.com/i/pkFpP41"><img src="https://s21.ax1x.com/2024/04/29/pkFpP41.png" alt="pkFpP41.png" border="0" /></a>


文件日志
<a href="https://imgse.com/i/pkFpF9x"><img src="https://s21.ax1x.com/2024/04/29/pkFpF9x.png" alt="pkFpF9x.png" border="0" /></a>


elastic日志

<a href="https://imgse.com/i/pkFpAgK"><img src="https://s21.ax1x.com/2024/04/29/pkFpAgK.png" alt="pkFpAgK.png" border="0" /></a>


mongo日志


<a href="https://imgse.com/i/pkFpEjO"><img src="https://s21.ax1x.com/2024/04/29/pkFpEjO.png" alt="pkFpEjO.png" border="0" /></a>






<div> </div>
`````

--- **end of file: source/articles/c3.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c4.md** (project: nb_log) --- 

`````markdown
# 4.关于logging包日志观察者模式

不会扩展日志记录到什么地方，主要是不懂什么叫观察者模式

```python
# 例如 日志想实现记录到 控制台、文件、钉钉群、redis、mongo、es、kafka、发邮件其中的几种的任意组合。
# low的人，会这么写，以下是伪代码，实现记录到控制台、文件、钉钉群这三种的任意几种组合。

def 记录到控制台(msg):
    """实现把msg记录到控制台"""


def 记录到文件(msg):
    """实现把msg记录到文件"""


def 记录到钉钉(msg):
    """实现把msg记录到钉钉"""


def 记录到控制台和文件(msg):
    """实现把msg记录到控制台和文件"""


def 记录到控制台和钉钉(msg):
    """实现把msg记录到控制台和钉钉"""


def 记录到文件和钉钉(msg):
    """实现把msg记录到文件和钉钉"""


def 记录到控制台和文件和钉钉(msg):
    """实现把msg记录到控制台和文件和钉钉"""


# 当需要把msg记录到文件时候，调用函数 记录到文件(msg)
# 当需要把msg记录到控制台时候，调用函数 记录到控制台(msg)
# 当需要把msg记录到钉钉时候，调用函数 记录到钉钉(msg)
# 当需要把msg记录到控制台和文件，调用函数 记录到控制台和文件(msg)
# 当需要把msg记录到控制台和钉钉，调用函数 记录到控制台和钉钉(msg)
# 当需要把msg记录到控制台和文件和钉钉，调用函数 记录到控制台和文件和钉钉(msg)

"""
这样会造成，仅记录到控制台 文件 钉钉这三种的任意几个，需要写6个函数，调用时候需要调用不同的函数名。
但是现在日志可以记录到8种地方，如果还这么low的写法，需要写8的阶乘个函数，调用时候根据场景需要会调用8的阶乘个函数名。
8的阶乘结果是 40320 ，如果很low不学设计模式做到灵活组合，需要多写 4万多个函数，不学设计模式会多么吓人。

"""
```

##### 观察者模式图片

![Image text](https://www.runoob.com/wp-content/uploads/2014/08/observer_pattern_uml_diagram.jpg)

菜鸟教程的观察者模式demo连接
[观察者模式demo](https://www.runoob.com/design-pattern/observer-pattern.html)

这个uml图上分为Subject 和 基类Observer，以及各种继承或者实现Observer的XxObserver类，
其中每个不同的Observer需要实现doOperation方法。

如果对应到python内置的logging日志包的实现，那么关系就是：

Logger是uml图的Subject

loging.Handler类是uml图的Observer类

StreamHandler FileHandler DingTalkHandler 是uml图的各种XxObservers类。

StreamHandler FileHandler DingTalkHandler类的 emit方法是uml图的doOperation方法

只有先学设计模式，才能知道经典固定套路达到快速看代码，能够达到秒懂源码是怎么规划设计实现的。

如果不先学习经典设计模式，每次看包的源码，需要多浪费很多时间看他怎么设计实现的，不懂设计模式，会觉得太难了看着就放弃了。

在python日志的理解和使用上，国内能和我打成平手的没有几人。




<div> </div>
`````

--- **end of file: source/articles/c4.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c5.md** (project: nb_log) --- 

`````markdown
# 5.演示不懂观察者模式，日志重复记录惨烈的例子

## 5.1 演示一个由于不好好理解观察者模式，封装的日志类在调用时候十分惨烈的例子，惨烈程度达到10级。

这个是真实发生的例子。

这个例子是为了记录10万次日志到控制台和文件，就算python性能很差，就这个例子而言，预期耗时肯定是需要10秒以内才算合格。

看起来10秒内可以运行完成，实际上1周内能运行结束这个代码，我愿意吃10斤翔。

```python
"""
演示重复，由于封装错误的类造成的。模拟一个封装严重失误错误的封装例子。

看起来10秒内可以运行完成，实际上1周内能运行结束这个代码，我愿意吃10斤翔。

这个代码惨烈程度达到10级。明明是想记录10000次日志，结果却记录了 10000 * 10001 /2 次。
如果把f函数调用100万次，那么控制台和文件将会各记录5000亿次，日志会把代码拖累死。
不好好理解观察者模式有多惨烈。因为反复添加观察者（handler）,
导致第1次调用记录1次，第二次调用时候记录2次，第10次调用时候记录10次，这成了高斯求和算法了。

这种类似的封装造成的后果可想而知，长期部署运行后，不仅项目代码性能几乎被日志占了99%，还造成磁盘被弄爆炸。
"""
import logging
import time


class LogUtil:
    def __init__(self):
        self.logger = logging.getLogger('a')
        self.logger.setLevel(logging.DEBUG)
        self._add_stream_handler()
        self._add_file_handler()

    def _add_stream_handler(self):
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(fmt="%(asctime)s-%(name)s-%(levelname)s-%(message)s"))
        self.logger.addHandler(sh)

    def _add_file_handler(self):
        fh = logging.FileHandler('a.log')
        fh.setFormatter(logging.Formatter(fmt="%(asctime)s-%(name)s-%(levelname)s-%(message)s"))
        self.logger.addHandler(fh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)


def f(x):
    log = LogUtil()  # 重点是这行，写在了函数内部。既没有做日志命名空间的handlers判断控制，封装的类本身也没写单利或者享元模式。
    log.debug(x)


t1 = time.time()
for i in range(100000):
    f(i)

print(time.time() - t1)

```

## 5.2 使用博客园搜索后排名第一个的python 日志封装，也是严重重复记录。

[博客园 python 日志封装](https://www.cnblogs.com/linuxchao/p/linuxchao-logger.html)

```python
import logging


class Log(object):
    def __init__(self, name=__name__, path='mylog.log', level='DEBUG'):
        self.__name = name
        self.__path = path
        self.__level = level
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level)

    def __ini_handler(self):
        """初始化handler"""
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.__path, encoding='utf-8')
        return stream_handler, file_handler

    def __set_handler(self, stream_handler, file_handler, level='DEBUG'):
        """设置handler级别并添加到logger收集器"""
        stream_handler.setLevel(level)
        file_handler.setLevel(level)
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    def __set_formatter(self, stream_handler, file_handler):
        """设置日志输出格式"""
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                      '-%(levelname)s-[日志信息]: %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    def __close_handler(self, stream_handler, file_handler):
        """关闭handler"""
        stream_handler.close()
        file_handler.close()

    @property
    def Logger(self):
        """构造收集器，返回looger"""
        stream_handler, file_handler = self.__ini_handler()
        self.__set_handler(stream_handler, file_handler)
        self.__set_formatter(stream_handler, file_handler)
        self.__close_handler(stream_handler, file_handler)
        return self.__logger


if __name__ == '__main__':
    def f():
        log = Log(__name__, 'file.log')
        logger = log.Logger
        # logger.debug('I am a debug message')
        # logger.info('I am a info message')
        # logger.warning('I am a warning message')
        # logger.error('I am a error message')
        logger.critical('I am a critical message')


    for i in range(10):
        f()
```

```
运行上面这个代码，应为调用了f函数10次，应该是一共打印10次和写入文件10次，结果是打印55次，写入文件55次。
因为这个实例化写在了函数内部，造成每调用一次就新增一次handler，日志记录的总次数不是预期期待的变成了高斯求和。
这种日志封装很惨，如果部署线上，f函数调用了10万次，那么会造成重复记录  100000*100001/2次变成50亿次，
随着程序部署的时间越来越长，服务器cpu会越来越卡，磁盘增长也会越来越快，而且问题难以排查，造成事故会非常惨烈。


千万别说你会注意，只会把Log封装类实例化放在函数的外面，这样做没用的，一个项目几百个模块，
如果在很多个模块级下面都实例化相同命名空间的日志，然后使用run.py调用了几百个模块作为运行起点，一样会造成重复打印。
所以只是小心翼翼的吧日志类的实例化放在模块级下面，仍然会发生重复记录的可能，只不过没有for循环那么惨烈的高斯求和叠加出记录那么多。
但是使用nb_log就可以随便你怎么折腾，放在for循环下面无限实例化都不怕不会重复记录日志。
```

## 5.3 使用火热的loguru 来演示惨烈的文件日志重复记录。

```python
"""
这也是一个很惨烈的真实例子。使用大火的 loguru ，然来用户让来本意是想实现每天生成一个新的日志文件。
结果造成了在所有历史文件中都重复记录当前日志，随着部署的天数越来越长，长时间例如半年 八九个月 如果不重新部署程序，
会造成严重的磁盘紧张和cpu飙升。
"""

from loguru import logger
import time


def f(x):
    """
     用户实际生产是想每一天生成一个日志， time.strftime("%Y-%m-%d")}.log，
     但这里为了节约时间方便演示文件日志重复记录所以换成时分秒演示，不然的话要观察很长的时间每隔一天观察一次才能观察出来。
    """
    logger.add(f'test_{time.strftime("%H-%M-%S")}.log')
    logger.debug(f'loguru 太惨了重复记录 {x}')
    logger.info(f'loguru 太惨了重复记录 {x}')
    logger.warning(f'loguru 太惨了重复记录 {x}')
    logger.error(f'loguru 太惨了重复记录 {x}')
    logger.critical(f'loguru 太惨了重复记录 {x}')


for i in range(100):
    time.sleep(1)
    f(i)

"""
预期是每秒调用一次函数f，但函数里面面有5次记录，debug info warning error  critical，
所以预期是每秒有5条日志只写入当前最新的日志文件中，但结果是每秒都写入到历史所有日志文件中。
只看当前最新的那个日志文件，似乎没有看到重复记录，但如果看所有的历史旧日志文件可以看到每个旧文件都严重重复记录了。
这种问题很难排查，所以用日志要谨慎，要搞懂日志handlers，和设计模式的观察者模式才能用好日志。
"""
```


<div> </div>


`````

--- **end of file: source/articles/c5.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c6.md** (project: nb_log) --- 

`````markdown
# 6. 对比 loguru 10胜

nb_log对比 loguru，必须对比，如果比不过loguru就不需要弄nb_log浪费精力时间

## 6.1 先比控制台屏幕流日志颜色，nb_log三胜。

这是loguru 屏幕渲染颜色
[![hZC2PU.png](https://z3.ax1x.com/2021/08/25/hZC2PU.png)](https://imgtu.com/i/hZC2PU)

1）nb_log 颜色更炫

2）nb_log 自动使用猴子补丁全局改变任意print

3）nb_log 支持控制台点击日志文件行号自动打开并跳转到精确的文件和行号。

## 6.2 比文件日志性能，nb_log比loguru快400%。

```
nb_log为了保证多进程下按大小安全切割，采用了文件锁 + 自动每隔1秒批量把消息写入到文件，大幅减少了加锁解锁和判断时候需要切割的次数。
nb_log的file_handler是史上最强的，超过了任何即使不切割文件的内置filehandler,比那些为了维护自动切割的filehandler例如logging内置的
RotatingFileHandler和TimedRotatingFileHandler的更快。比为了保证多进程下的文件日志切割安全的filehandler更是快多了。

比如以下star最多的，为了确保多进程下切割日志文件的filehandler  
https://github.com/wandaoe/concurrent_log
https://github.com/unlessbamboo/ConcurrentTimeRotatingFileHandler
https://github.com/Preston-Landers/concurrent-log-handler

nb_log的多进程文件日志不仅是解决了文件切割不出错，而且写入性能远超这些4到100倍。
100倍的情况是 win10 + https://github.com/Preston-Landers/concurrent-log-handler对比nb_log
nb_log的文件日志写入性能是loguru的4倍，但loguru在多进程运行下切割出错。
```

### 6.2.1 loguru快速文件写入性能，写入200万条代码

这个代码如果rotation设置10000 Kb就切割，那么达到切割会疯狂报错，为了不报错测试性能只能设置为1000000 KB

```python
import time

from loguru import logger
from concurrent.futures import ProcessPoolExecutor

logger.remove(handler_id=None)

logger.add("./log_files/loguru-test1.log", enqueue=True, rotation="10000 KB")


def f():
    for i in range(200000):
        logger.debug("测试多进程日志切割")
        logger.info("测试多进程日志切割")
        logger.warning("测试多进程日志切割")
        logger.error("测试多进程日志切割")
        logger.critical("测试多进程日志切割")


pool = ProcessPoolExecutor(10)
if __name__ == '__main__':
    """
    100万条需要115秒
    15:12:23
    15:14:18
    
    200万条需要186秒
    """
    print(time.strftime("%H:%M:%S"))
    for _ in range(10):
        pool.submit(f)
    pool.shutdown()
    print(time.strftime("%H:%M:%S"))
```

### 6.2.2 nb_log快速文件写入性能，写入200万条代码

```python
from nb_log import get_logger
from concurrent.futures import ProcessPoolExecutor

logger = get_logger('test_nb_log_conccreent', is_add_stream_handler=False, log_filename='test_nb_log_conccreent.log')


def f(x):
    for i in range(200000):
        logger.warning(f'{x} {i}')


if __name__ == '__main__':
    # 200万条 45秒
    pool = ProcessPoolExecutor(10)
    print('开始')
    for i in range(10):
        pool.submit(f, i)
    pool.shutdown()
    print('结束')
```

## 6.3 多进程下的文件日志切割，nb_log不出错，loguru出错导致丢失大量日志。

```
将10.2的代码运行就可以发现，loguru设置了10M大小切割，疯狂报错，因为日志在达到指定大小后切割需要备份重命名，
造成其他的进程出错。

win10 + python3.6 + loguru 0.5.3(任何loguru版本都报错，已设置enqueue=True)
出错如下。
Traceback (most recent call last):
  File "F:\minicondadir\Miniconda2\envs\py36\lib\site-packages\loguru\_handler.py", line 287, in _queued_writer
    self._sink.write(message)
  File "F:\minicondadir\Miniconda2\envs\py36\lib\site-packages\loguru\_file_sink.py", line 174, in write
    self._terminate_file(is_rotating=True)
  File "F:\minicondadir\Miniconda2\envs\py36\lib\site-packages\loguru\_file_sink.py", line 205, in _terminate_file
    os.rename(old_path, renamed_path)
PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问。: 'F:\\coding2\\nb_log\\tests\\log_files\\loguru-test1.log' -> 'F:\\coding2\\nb_log\\tests\\log_files\\loguru-test1.2021-08-25_15-12-23_434270.log'
--- End of logging error ---
```

```
python性能要发挥好，必须开多进程。
例如django flask的部署用gunicorn uwsgi都是自动开多进程+线程(协程)，即使你的代码里面没亲自写多进程运行，但是自动被迫用了多进程。
即使你代码没亲自写多进程，例如在同一个机器反复把xx.py启动部署10次，相当于10个进程的日志都写到 yyyy.log,一样是被迫相当于10个进程了。
所以多进程文件日志切割安全很重要。

有的人说自己多进程写文件日志没出错，那是你没设置成按大小或者时间切割，或者自己设置了1G大小切割或者按天切割，不容易观察到。
只要你把时间设置成每1分钟切割或者10M切割，就会很快很容易观察到了。
如果文件日志不进行切割，多进程写同一个文件不会出错的。
```

## 6.4 写入不同的文件，nb_log采用经典日志的命名空间区分日志，比loguru更简单

```python
from nb_log import get_logger
from loguru import logger

# nb_log 写入不同的文件是根据日志命名空间 name 来区分的。方便。
logger_a = get_logger('a', log_filename='a.log', log_path='./log_files')
logger_b = get_logger('b', log_filename='b.log', log_path='./log_files')
logger_a.info("嘻嘻a")
logger_b.info("嘻嘻b")

# loguru 不同功能为了写入不同的文件，需要设置消息前缀标志。不方便。
logger.add('./log_files/c.log', filter=lambda x: '[特殊标志c!]' in x['message'])
logger.add('./log_files/d.log', filter=lambda x: '[特殊标志d!]' in x['message'])
logger.add('./log_files/e.log', )
logger.info('[特殊标志c!] 嘻嘻c')  # 出现在c.log和 e.log  消息为了写入不同文件需要带消息标志
logger.info('[特殊标志d!] 嘻嘻d')  # 出现在d.log和 e.log  消息为了写入不同文件需要带消息标志
```

## 6.5 按不同功模块能作用的日志设置不同的日志级别。loguru无法做到。

例如a模块的功能希望控制台日志可以显示debug，b模块的功能只显示info以上级别。

```python
import logging
from nb_log import get_logger

# nb_log 写入不同的文件是根据日志命名空间 name 来区分的。方便。
logger_a = get_logger('a', log_level_int=logging.DEBUG)
logger_b = get_logger('b', log_level_int=logging.INFO)
logger_a.debug("嘻嘻a debug会显示")
logger_a.info("嘻嘻a info会显示")
logger_b.debug("嘻嘻b debug不会显示")
logger_b.info("嘻嘻b info会显示")
```

## 6.6 nb_log内置自带的log handler种类远超loguru

```
nb_log 内置的handler包括 钉钉 elastic kafka，方便自动一键把日志同时记载到这些地方。
loguru没有内置，loguru的add方法以文件日志为核心。
```

## 6.7 比第三方的日志handler扩展数量，nb_log完胜loguru

```
日志能记载到什么地方是由handler决定的，很多人以为日志等于控制台 + 文件，并不是这样的。
日志可以记载到任何介质，不是只有控制台和文件。
nb_log的核心方法是get_logger，此方法是返回原生loggin.Logger类型的对象，
原生日志可扩展的第三方handler包在pypi官网高达几百个，可以直接被nb_log使用。
```

## 6.8 nb_log的get_logger返回类型是原生经典logging.Logger，兼容性达到了100%。loguru独立实现日志系统，兼容性很差。

```
绝大部分python代码采用的是内置经典的python logging模块，
例如老代码 
logger = logging.getLogger("my_namespage")

老代码的其他地方使用了logger对象的这些方法，远不止这两个。
logger.setLevel()
logger.addHandler()

如果是改成nb_log,  logger = nb_log.get_logger("my_namespage")
那么logger.setLevel() logger.addHandler() 仍然可以正常使用。

如果是改成loguru， from loguru import logger
那么logger.setLevel() logger.addHandler() 会是代码报错，因为loguru的logger对象是独立特行独自实现的类型，没有这些方法。
```

## 6.9 易用性对比，nb_log的控制台和文件handler比loguru添加更容易

```
loguru哪里好了？
loguru只是自动有好看的日志formatter显示格式 + 比原生logger更容易添加文件handler。
loguru比原生logging也只是好在这两点而已，其他方面这不如原生。

nb_log 比loguru添加控制台和文件日志更简单，并且显示格式更炫。loguru对比原生logging的两个优势在nb_log面前没有了。
```

原生日志设置添加控制台和文件日志并设置日志格式是比loguru麻烦点，但这个麻烦的过程被nb_log封装了。

[![hZ2HJg.png](https://z3.ax1x.com/2021/08/25/hZ2HJg.png)](https://imgtu.com/i/hZ2HJg)

## 6.10 nb_log可以灵活捕获所有第三方python包、库、框架的日志,loguru不行

```
不知道大家喜欢看三方包的源码不，或者跳转进去看过三方包源码不，
95%的第三方包的源码的大量文件中都有写   logger = logging.getLogger(__name__)  这段代码。
假设第三包的包名是  packagex, 这个包下面有 ./dira/dirb/yy.py 文件，
假设logger = logging.getLogger(__name__)  这段代码在 ./dira/dirb/moduley.py文件中，
当使用这个三方包时候，就会有一个 packagex.dira.dirb.yy.moduley 的命名空间的日志，如果你很在意这个模块的日志，
希望吧这个模块的日志捕获出来，那么可以 logger = logging.getLogger("packagex.dira.dirb.moduley"),
然后对logger添加文件和控制台等各种handler，设置合适的日志级别，就可以显示出来这个模块的日志了。

为什么第三方包不默认给他们自己的logger添加handler呢，这是因为第三方包不知道你喜欢吧日志记载到哪里，而且第三包不知道你会很关心这个模块的日志，
如果每隔第三方包都那么自私，把日志默认添加handler，并且设置成info或debug级别，那各种模块的日志加起来就会很多，干扰用户。很多用户又不知道如何移除handler，
所以三方包都不会主动添加handler，需要用户自己去添加handler和设置用户喜爱的formattor。

代码例子如下，因为requests调用了urllib3，这里有urllib3的命名空间的日志，只是没有添加日志handler所以没显示出来。
nb_log.get_logger 自动加上handler和设置日志模板了，方便你调试你所关心的模块的日志。
```

```python
from nb_log import get_logger
import requests

get_logger('urllib3')  # 也可以更精确只捕获 urllib3.connectionpool 的日志，不要urllib3包其他模块文件的日志
requests.get("http://www.baidu.com")
```

<a href="https://imgtu.com/i/hJbkrD"><img src="https://z3.ax1x.com/2021/08/30/hJbkrD.png" alt="hJbkrD.png" border="0" /></a>
 
### 6.10.b 日志的命名空间意义很重要 ，就是那个logging.getLogger的入参，很多人还不懂。

```
如果日志名字是  a.b.c
那么 logging.getLogger("a")可以捕获a文件夹下的所有子文件夹下的所有模块下的日志，
logging.getLogger("a.b")可以捕获a/b文件夹下的所有模块下的日志
logging.getLogger("a.b.c") 可以精确只捕获a/b/c.py 这个模块的日志
```

[![hJOYIH.png](https://z3.ax1x.com/2021/08/30/hJOYIH.png)](https://imgtu.com/i/hJOYIH)

![](https://visitor-badge.glitch.me/badge?page_id=nb_log)


<div> </div>
`````

--- **end of file: source/articles/c6.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c7.md** (project: nb_log) --- 

`````markdown
# 7 nb_log 捕获三方包的日志

准确来说不是捕获，是给三方包的logger加上handlers，三方包的logger没有观察者例如 streamHandler fileHanlder等，不会自动打印控制台和记录文件啥的。

## 7.1 nb_log 记录三方包日志的方法，requests举例子

一般三方包的每个模块都会写 logger = logging.getLogger(__name__)，很多人非常之蒙蔽对这句话。

这个是创建了当前 包名.文件夹名.模块名 的日志命名空间,但没有创建handler，所以里面 logger.info() 是不会被记录到的。

只有对这个命名空间的logger加上handlers后才会记录到各种地方。


```python
from nb_log import get_logger
import requests

get_logger('urllib3')  # 也可以更精确只捕获 urllib3.connectionpool 的日志，不要urllib3包其他模块文件的日志
requests.get("http://www.baidu.com")
```


<a href="https://imgtu.com/i/hJbkrD"><img src="https://z3.ax1x.com/2021/08/30/hJbkrD.png" alt="hJbkrD.png" border="0" /></a>
 



有的人要记录请求了什么，状态是什么，非要自己亲自写日志，那其实urllib3对每个请求和状态码都记录了，
并不需要用户去亲自再重复写logger.info("请求了什么url  耗时多少 状态码是什么")，这些都是多此一举，主要是用户不懂日志命名空间。
如上图，get_logger 对 urllib3 命名空间的日志加上了控制台handler后就会自动记录到请求了什么url和响应情况了，完全不需要用户修复写代码。

requests包会调用urllib3,urllib3包里面记录了日志请求什么了，所以上面是 get_logger('urllib3') 而不是 get_logger('requests'),
一般情况下 get_logger(name=三方包名就可以了)

## 7.2 nb_log还可以记录flask/django任意三方包

例如 get_logger(name="werkzeug",log_file_name='myfile.log') ,就会记录到请求flask服务端url的日志到控制台和myfile.log了。

一般情况下 get_logger(name=三方包名就可以了)，get_logger(name='flask') 就可以记录到前端请求的是什么url了，
但是flask是一个基于Python开发并且依赖jinja2模板和Werkzeug WSGI服务的一个微型框架,对于Werkzeug本质是Socket服务端,
其用于接收http请求并对请求进行预处理，所以 get_logger(name="werkzeug") 用于捕获日志，因为记录请求url的是在 werkzeug 包下面写的，
所以命名空间是 werkzeug.xx.yy 。

![img_1.png](img_1.png)

![img.png](img.png)

如果代码中不写  get_logger(name="werkzeug")

![img_2.png](img_2.png)

## 7.3 python日志命名空间是树形结构

假设三方包名是 thp，三方包根目录里面有 xx.py 和 yy.py，并且每个python文件是 logger = logging.getLogger(__name__) 的，
你如果想捕获thp包所有日志， get_logger('thp') 就好了。

如果你只想捕获 xx.py的debug以上日志， 捕获yy.py的error以上日志，那么应该写 
get_logger('thp.xx',log_level_int=10)  # 10就是 logging.DEBUG常量。
get_logger('thp.yy',log_level_int=40)  # 40就是 logging.ERROR常量。
 

python的日志命名空间是树形的，用 . 隔开。

假设 日志命名空间是 a.b.c, 那么 a 和a.b  和 a.b.c 都可以捕获 a.b.c 命名空间日志。


例如这个例子，第27行并不会被打印，但是第31行可以打印出来日志。因为a命名空间是a.b.c的父命名空间，a.b.c会先查找 a.b.c，再查找 a.b，再查找a，再查找根命名空间,一直向上查找。

根命名空间是所有一切命名空间的父命名空间。

1）这是给a命名空间加上handlers

![img_3.png](img_3.png)


2） 当name传 None时候意思是根命名空间加上handlers了。根命名空间是无敌的，会捕获所有三方包的日志，如果你不想捕获所有包的日志就别这么用。

![img_4.png](img_4.png)




## 7.4 如何确定有哪些日志命名空间的日志可以被记录，强大的 get_logger(None)

get_logger(None) 就可以给根命名空间机上handler了，然后控制台的日志会显示每个日志的命名空间，你把对你有作用的命名空间记录下来，没有作用的干扰日志就不需要记住那些命名空间了。

例如 flask我咋知道是 get_logger(name="werkzeug") 可以使用werkzeug来捕获请求url记录的？这个单词werkzeug太难拼写了，背诵不下来咋办，
那就是简单粗暴的 get_logger(None) 就可以了，然后前端请求url时候，你看到控制台日志会显示 werkzeug 命名空间了，
然后你再把get_logger(None) 换成 get_logger(name="werkzeug") 就好了。

requests请求时候，我咋知道是get_logger('urllib3') 而不是 get_logger('requests')来捕获请求url的地址和状态码，是一个道理。

线上不建议 get_logger(None) 这样做，这样项目三方包太多了，记录不关心的日志了。
希望用户传入精确的日志命名空间，给不同命名空间设置不同的日志级别和添加不同的handlers。

![img_5.png](img_5.png)

















<div> </div>
`````

--- **end of file: source/articles/c7.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c8.md** (project: nb_log) --- 

`````markdown
# 8 禁止对nb_log进行二次封装

## 8.1 禁止对nb_log进行以下形式的封装

不要偷梁换柱，把logger对象换成别的类。nb_log没有发明新的类型，get_logger是返回经典日志类型 logging.Logger，
如果你非要对nb_log封装，那应该返回  logging.Logger 类型，不要用其他类型的对象 .debug()  来记录日志，
要使用 logging.Logger 类型的对象 .debug() 来记录日志。


```doctest
禁止使用此种错误方式来封装 nb_log ，因为点击控制台跳转到的日志地方跳转到你的这个类了，而不是精确跳转到 logger.debug/info()  的地方
并且日志的name 千万不要固定死了，多命名空间才是日志精髓。
所有日志只能写入到mylog.log文件中，不能写入不同的文件,不能给每个日志设置不同的级别，不能自定义日志记录到控制台 文件 mongo中的哪些地方。
```

```python
import nb_log


class LogUtil:
    def __init__(self):
        self.logger = nb_log.get_logger('xx',log_filename='mylog.log')

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

if __name__ == '__main__':
    print('日志命名固定死了，没有多实例单独控制很差劲。所有日志只能写入到mylog.log文件中，不能写入不同的文件')
    logger = LogUtil()
    logger.debug('点击控制台不能跳转到本行，跳转到工具类去了')
    logger.info('点击控制台不能跳转到本行，跳转到工具类去了')
    logger.warning('点击控制台不能跳转到本行，跳转到工具类去了')
    logger.error('点击控制台不能跳转到本行，跳转到工具类去了')
    logger.critical('点击控制台不能跳转到本行，跳转到工具类去了')
```



有的人闲的蛋疼，非要装逼写个废物类，这样封装个废物类有什么必要性了?

nb_log.get_logger()  得到的是内置logging.Logger对象，兼容性无敌了，还能点击精确跳转到发生日志的文件和行号。
用户这样封装那有什么卵用了，增加了什么新功能了吗？
用户的 LogUtil() 得到的logger对象能 logger.setLevel(logging.WARN) 这样吗，一下子就报错了，因为不是经典日志类型。

用户封装nb_log后，把get_logger的入参全部屏蔽了，无法使用多命名空间，无法自定义不同的日志表现行为和记录到的地方，简直封装了个废物，越封装越差。
写类不是为了装逼，对nb_log和任意三方包能不封装就别封装。

### 8.1b 如果非要封装nb_log,为了保证获取的代码文件和行号是正确的，

生成logger时候要指定 logger_cls=nb_log.CompatibleLogger , (因为python3.9以下logging不支持设置日志位置的堆栈级别 stacklevel 入参)

并在你的debug方法调用原生logger对象的debug方法时候，加上 extra = {"sys_getframe_n": 3}



```python
import nb_log
logger = nb_log.LogManager('my_logger', logger_cls=nb_log.CompatibleLogger).get_logger_and_add_handlers(log_filename='my_logger.log')

def debug(msg)
    logger.debug(msg, extra = {"sys_getframe_n": 3})
```

## 8.2 其他废物封装举例子

包括之前举的例子，封装redis mysql的,有的人这样封装

```python
from redis import Redis

class MyRedis:
    def __init__(self):
        self.r = Redis()
        
    def my_set(self,k,v):
        self.r.set(k.v)
        
    def my_get(self,k):
        self.r.get(k)
        
    def my_delete(self,k):
        self.r.delete(k)
        
    
    def my_hget(self,name,key):
        self.r.hget(name,key)
    
        
        
    """ 继续废物封装几百个redis方法"""
    

```

三方Redis类不好吗，非要封装几千个方法，写几万行代码才开心。
这种封装自定义的 def my_xx() : 方法里面去调用 三方包核心对象.xx()的封装没有什么用，快别封装了。

<div> </div>




`````

--- **end of file: source/articles/c8.md** (project: nb_log) --- 

---


--- **start of file: source/articles/c9.md** (project: nb_log) --- 

`````markdown

# 9 nb_log常见疑问解答

## 9.1 怎么把普通debug info日志写入文件a，把错误级别日志写到文件b？

看文档 1.1.a2 介绍





## 9.2 没有使用pycahrm run运行，直接在linux或cmd运行，生成的nb_log_config.py 位置错误，或者导入不了nb_log_config模块


1.1.c中已经说明了：

项目中任意脚本使用nb_log,第一次运行代码时候，会自动在 sys.path[1] 目录下创建 nb_log_config.py文件并写入默认值。
之后nb_log 会自动 import nb_log_config, 如果import到这个模块了，控制台会提示读取了什么文件作为配置文件。

如果是 cmd或者linux运行不是pycharm，需要 设置 PYTHONPATH为项目根目录，这样就能自动在当前项目根目录下生成或者找到 nb_log_config.py了。

用户可以print(sys.path)  print(sys.path[1]) 来查看 sys.path[1]的值是什么就知道了。

连PYTHONPATH作用是什么都不知道的python小白，一定要看下面文章 。

[pythonpath作用介绍的文章](https://github.com/ydf0509/pythonpathdemo)


说明完全不看文档，到现在还不知道PYTHONPATH的python人员太懒惰low了，文章说了很多次掌握PYTHONPATH的用途和好处了。


## 9.4 pyinstaller 打包后运行报错，no such file nb_log_config_default.py

![img_10.png](img_10.png)

如上图报错，

是因为导入不了 nb_log_config 模块，因为nb_log包是动态 importlib('nb_log_config')的，所以不能检测到需要打包nb_log_config.py

需要在pyinstaller打包时候生成的spec文件中去定义 hiddenimports 的值， hiddenimports=['nb_log_config'] ，
这样就会打包包括nb_log_config.py了，不会去自动新建配置文件了。

![img_11.png](img_11.png)

pyinstaller 使用spec文件来打包exe。  pyinstaller xxxx.spec 就可以了。

百度吧，连pyinstaller的spec文件的意义是什么都不知道就非要去打包，要先学习pystaller用法。


### 9.4.2 打包报错 no such file nb_log_config_default.py，解决方式2

只要在你的代码中写上 import nb_log_config ，那么打包就会自动包括了，这样就不需要在spec文件中去定义 hiddenimports 的值了。

<div> </div>

## 9.5 怎么屏蔽和打开某一部分日志？（选择性关闭和打开某部分日志）

不懂日志命名空间的是不可能精通怎么设置日志级别的。

<pre style="font-size: large;color: greenyellow;background-color: #0c1119">
有的人真的很头疼，老是问这种基础的低级问题，比如funboost的日志级别如何调，如何做到希望显示某个函数/模块的debug打印，但却又要关闭另一个模块/函数的info打印？
任何python日志只要是logging包实现的，日志就可以设置不显示和设置打开。

老是问这种问题，主要是不懂日志命名空间基本概念，尽管文档已经重复了不下50次这个名词，还是再在解答章节统一再啰嗦一次,说了无数次这个logging.getLogger第一个入参的意义，这就是文档长的原因。

这个问题从最基本的日志树形命名空间说起必须，不去了解日志name入参作用的人，永远搞不懂怎么关闭和打开特定日志，也不可能从根本性知道为什么不用print而要用日志。
</pre>

<pre style="font-size: large;color: #FFFF66;background-color: #0c1119">
在文档 1.6和 1.9 中就已经说明了， nb_log.get_logger  以及官方内置的 logging.getLogger 函数的第一个入参的name作用和意义了，
第一个入参作用是什么，这是python官方日志的重要特性，包括java语言的日志也是这样的，
如果连日志的name是什么都完全不知道，那就别说自己会使用日志了，请不要使用日志了，干脆自己封装个函数里面print和file.write算了，不懂name的作用的情况下使用日志毫无意义，不如print到底算了。
日志命名空间是python官方日志以及任何语言的最基本作用。

在nb_log文档中搜索 命名空间，会有很多讲解日志命名空间作用的，有的人嫌弃文档长，主要是花了很大篇幅讲解日志命名空间，这是官方日志的基本知识，
主要是有的人完全不懂官方内置日志的logging.getLogger(name) 入参的意义，所以造成文档长。
因为 nb_log使用的是官方logging实现的，于第三方包和各种扩展兼容性无敌， nb_log.get_logger 和 logging.getLogger 函数返回的都是原生logging.Logger对象，
所以兼容性无敌，这一点上远远的暴击loguru这种独立实现的logger对象。

</pre>


### 9.5.1 真实代码例子，说明怎么屏蔽某个日志。


假设下面这段代码是三方包里面的

logger_a 和logger_b 是三方包里面的日志，你要调整日志级别，不可能去骚操作去三方包里面的源码修改日志级别吧？

三方包里面的代码，packege1.py


```python
import logging
from nb_log import get_logger

"""
logging.DEBUG 是个常量枚举，值是10
logging.INFO 是个常量枚举，值是20
logging.WARNING 是个常量枚举，值是30
logging.ERROR 是个常量枚举，值是40
logging.CRITICAL 是个常量枚举，值是50

用数字和常量枚举都可以。
"""


logger_a = get_logger('aaaa',log_level_int=logging.INFO)

logger_b = get_logger('bbbb',log_level_int=20)

def funa():
    logger_a.info('模拟a函数里面啰嗦打印你不关心的日志aaaaa')

def funb():
    logger_b.info('模拟b函数里面，对你来说很重要的提醒日志打印日志bbbbb')
```


你的原来代码，调用函数funa。啰嗦输出 模拟a函数里面啰嗦打印你不关心的日志aaaaa 这句话到控制台  x1.py

```python
import funa,funb
funa()
funb()
```

![img_12.png](img_12.png)

优化日志级别后的代码,这个代码的调用funa函数将不再啰嗦的输出INFO级别日志打扰你了,funb函数仍然正常的输出INFO日志。  x2.py

```python
import funa,funb
logging.getLogger('aaaa').setLevel(logging.ERROR)  # 这里为什么入参是 aaaa 特别特别重要，如果不懂这个入参，你压根就不会调日志级别。
funa()
funb()
```

![img_13.png](img_13.png)

```
可以看到日志是灵活的，非常方便的关闭和打开日志，如果三方包在源码里面使用的是print，请问你如何打开或屏蔽某段打印？
还有就是日志命名空间了，有的人压根不懂日志命名空间，为什么我这个例子可以实现 打印funb里面的INFO日志，而关闭funa里面的INFO日志，希望你好好想明白。

为什么是 logging.getLogger('aaaa').setLevel(logging.ERROR)，
如果你是写的代码是 logging.getLogger('cccc').setLevel(logging.ERROR) 会屏蔽funa里面的INFO日志吗？自己好好想想。

```

### 9.5.2 你如何知道日志的命名空间 (name) 是什么?

```
你需要点击到源码去看日志的 getLogger 的name入参是什么吗，答案是否定的。
例如9.5.1 ，你是如何知道要写 logging.getLogger('aaaa').setLevel(logging.ERROR)，
你要咋知道 写 aaaa 而不是其他？ 这个在运行结果截图中已经显示了，nb_log的大部分日志模板的时间后面的 - xxxx - 就是指的日志name。

总结下如何知道日志的name的

1、看源码，看生成logger对象的地方的第一个入参
2、看控制台的日志模板
3、对那个logger.info的logger对象，加个print(logger.name),你就知道他的name了

```

### 9.5.3 经常看到三方包中写 logger = logging.getLogger(\__name\__) 啥意思？这个logger对象的name命名空间是什么？

```
logger = logging.getLogger(__name__) 是非常非常常见的写法，三方包里面大多数是这样，用户自己写的项目代码最好也可以是这样，这个好处非常多，
这种日志命名空间，一看就知道是什么文件夹下的什么python文件下的日志。
```

假设三方包 package1 的目录如下：
```
package1
     dir2
        module3.py


在 module3.py 源码中写 logger = logging.getLogger(__name__)，
此时logger对象还没有添加各种handlers，所以info及以下级别的日志默认就是不会显示的，如果已经添加了handlers后，就会显示日志了。

那么你要如何屏蔽或者捕获日志呢，主要还是要知道命名空间，因为源码写入参的是 __name__，所以你是不是不知道他的命名空间是什么了，这个也是python基础，

你只要 logging.getLogger('package1.dir2.module3').setLevel(logging.ERROR) 就能调高module3.py中的日志界别了。
你也可以 logging.getLogger('package1.dir2').setLevel(logging.ERROR)，这是调高 package1/dir2文件夹下所有python文件的日志级别。
你也可以 logging.getLogger('package1').setLevel(logging.ERROR)，这是调高 package1包里面的一切python文件的日志级别。
日志命名空间是树形的，假设 a.b.c ，那么a.b.c 和 a.b 和 a 都可以 对他设置命名空间和添加handlers。

因为 __name__ 在自己当前运行模块的值是 "__main__",
如果某个模块被其他地方导入，作为被导入模块，在其他地方看来，他的  __name_ 就是 把文件夹路径名的 / 换成. ,然后去掉.py。这是python基本常识。

```

### 9.5.4 日志命名空间是树形的
```
logger的name如果是 a.b.c， 只要你在a.b加上handler 或者a上加上handlers，a.b.c的日志就可以被记录。
因为日志命名空间使用 . 分割 a.b是a.b.c的父命名空间，a是a.b的的父命名空间。

如果你想 a.b.d 显示debug以上日志，a.b.c 显示info以上日志 ，那就需要精细化设置 a.b.d 和a.b.c的日志为不同级别了，不能只设置a.b，那就没法区分这两个命名空间的日志级别了。

现在知道 logger = logging.getLogger(__name__) 了吧， __name__ 是天然的树形日志命名空间。 
例如celery三方包的 celery/worker/consumer/connection.py 里面如果写 logger = logging.getLogger(__name__)， 那么日志命名空间就自动是  celery.worker.consumer.connection 了，这就是一个树形命名空间了。
粗暴一点 getLogger("celery") 对 celery整体设置日志级别，也可以 getLogger('celery.worker.consumer.connection') 精细化对celery每个不同的模块设置为不同的日志级别
```


### 9.5.5 举个例子，如何打开某个日志显示(和屏蔽日志相反)

requests请求百度，requests使用的是urllib3封装的，urllib3中已经有日志已经记录了请求状态码和url了。只需要给urllib3添加handlers就行了。

```
nb_log.get_logger(name)是对应原生logging包的，
logger=logging.getLogger(anme)
handler = xxHandler()  
formatter = Formatter()
handler.setFormatter(formatter)  
logger.addHnalder(handler) 的全流程封装。  

不懂日志的人，还需要自己封装搞个请求函数，在请求函数里面加日志，自己去手写记录请求了什么rul 响应状态码是什么，那是你不懂日志和命名空间，所以你需要脱了裤子放屁。
```

![img_15.png](img_15.png)

```
从日志可以看到，记录请求url和状态码的日志命名空间是 urllib3.connectionpool, 但是上面9.5.4讲了，日志命名空间是树形的，
所以你只需要对 urllib3 设置debug级别，并加上handlers后， urllib3.connectionpool 命名空间的debug级别 以上就可以被记录到了。
```

### 9.5.6 nb_log 提前锁定日志级别的方式

有的日志 logger对象 是随着 类实例化时候动态创建的，不方便去修改日志级别。 
因为有的日志是动态的在函数或者内里面去创建logger和设置日志级别。如果你提前设置日志级别，还是会被动态调用时候生成的logger的日志级别覆盖掉，

nb_log提供了提前锁定日志级别的方法，nb_log通过猴子补丁patch了 logging.Logger.setLevel方法，

使用 nb_log.LogManager('name1').preset_log_level(20) 可以给某个命名空间提前锁定日志级别，锁定日志级别后，后续再修改他的级别会使设置无效。

nb_log.LogManager('name1').preset_log_level(20) 比官方自带的设置日志级别方法 setLevel  的 nb_log.LogManager('name1').setLevel(20) 更强力，
preset_log_level是锁定日志级别，后续无法再对name1命名空间修改日志级别；而setLevel 设置日志级别后，后续还可以修改日志级别。


代码例子：

```python

import logging
import nb_log

nb_log.LogManager('name1').preset_log_level(20)  # preset_log_level 提前设置锁定日志级别为20(logging.INFO)

logger = nb_log.get_logger('name1',log_level_int=logging.DEBUG) # 设置级别为debug操作失效
# logger.setLevel(10) # 设置级别为debug操作失效
logger.debug('啊啊啊')  # 由于已经提前锁定了日志级别为INFO，后续再修改级别为DEBUG无效，所以这个logger.debug日志不会显示。
```

### 9.5.7 print或logger消息中包括某些字符串，屏蔽打印的设置

```
在 nb_log_config.py 配置文件中的FILTER_WORDS_PRINT 填写  FILTER_WORDS_PRINT = ["测试过滤字符串的呀", "阿弥陀佛", "善哉善哉"]，那么消息中包含数组中任何一个字符串，消息将不会打印出来。
以下为例子。
```

```python
import nb_log

logger = nb_log.get_logger('test_name')

str1 = '我们一起练习 阿弥陀佛'
str2 = '啦啦啦德玛西亚'
str3 = '嘻嘻 善哉善哉的'

print(str1)
print(str2)
print(str3)

logger.info(str1)
logger.info(str2)
logger.info(str3)

```

结果如图

![img_16.png](img_16.png)


### 9.5.8 nb_log 大量使用猴子补丁的原理


实现控制台消息过滤的原理是对 sys.stdout.write 打了猴子补丁。

```python

from nb_log import nb_log_config_default


def _need_filter_print(msg: str):
    for strx in nb_log_config_default.FILTER_WORDS_PRINT:
        if strx in str(msg):
            return True  # 过滤掉需要屏蔽的打印
    return False

sys_stdout_write_raw = sys.stdout.write  # 保存原来的

def _sys_stdout_write_monkey(msg: str):
    if _need_filter_print(msg):
        return
    else:
        sys_stdout_write_raw(msg)


sys.stdout.write = _sys_stdout_write_monkey  # 对 sys.stdout.write 打了猴子补丁。使得可以过滤包含指定字符串的消息。

```

```
这就是猴子补丁，不修改源代码，不仅可以对三方包进行修改，还可以对内置模块就行修改。有的人到现在还不知道怎么使用猴子补丁。
有的人把猴子补丁当做是gevent包特有的，这是错误的，任何人都可以开发和使用猴子补丁。
```

#### 9.5.8.2 怎么开发猴子补丁？例如 mod.py有代码如下 (与nb_log无关,跑题了)
```python
def fa():
    print('hello')

def fb():
   print('start')
   fa()
   print('end')
```

```
你希望调用 mod.fb() 打印出现 start hi end,  笨的人就去修改 mod.py 的源码的 fa 函数，改成 print('hi'),
每个python安装环境都要去修改源码，和你合作项目的同事也要去修改自己电脑的python安装包路径的源码，这样太low了。
牛的人就是使用猴子补丁,定义一个函数,然后让三方包的函数连接到你的函数，使得调用三方包函数行为发生动态变化。
```

```python
import mod
def my_fa():
    print('hi')
    
mod.fa = my_fa

mod.fb()
```

```
然后调用 mod.fb()就会打印 start hi end ，而不是 start hello end。
有的人不知道怎么开发和使用猴子补丁，造成写代码太忙了



```

## 9.6 ImportError: DLL load failed while importing win32file: 找不到指定的程序。 解决方式

```
1.
如果遇到ImportError: DLL load failed while importing win32file: 找不到指定的程序。

运行 pywin32_postinstall.py 程序，如下面例子，按需修改成你的python解释器路径就好了

D:/ProgramData/Miniconda3/envs/py39b/python.exe   D:/ProgramData/Miniconda3/envs/py39b/Scripts/pywin32_postinstall.py -install


运行 pywin32_postinstall.py 如果提示 进程有占用，杀死python程序先。
taskkill /F /IM python.exe


2. win上尽量使用 cmd运行，不要使用powershell运行Python代码。
 PowerShell 和 CMD 的环境变量处理方式不同。PowerShell 可能没有正确继承或加载某些系统环境变量，特别是与 Python 和 pywin32 相关的路径。

```

## 9.7 怎么使用原生 print 来打印不带时间 文件行号的 纯净字符串？

有时候偶尔需要在打印日志时，打印不带时间 文件行号的 纯净字符串，

- 方式一：  
   把 nb_log_config.py 配置文件中设置 AUTO_PATCH_PRINT = False ，适合所有print都不被打猴子补丁。

- 方式二：  
   如果你想给print打猴子补丁，但有时偶尔需要原生的print效果打印纯净的字符串，   
   from nb_log import stderr_raw,stdout_raw,print_raw   
   print_raw("现在这个字符串不会被转换成 带时间 行号的打印了，此条打印是原生print效果")   


`````

--- **end of file: source/articles/c9.md** (project: nb_log) --- 

---

# markdown content namespace: nb_log codes 


## nb_log File Tree (relative dir: `nb_log`)


`````

└── nb_log
    ├── __init__.py
    ├── add_python_executable_dir_to_path_env.py
    ├── capture_warnings.py
    ├── direct_logger.py
    ├── exception_auto_log.py
    ├── file_write.py
    ├── formatters.py
    ├── frequency_control_log.py
    ├── global_except_hook.py
    ├── handlers.py
    ├── handlers_concurrent_rotating_file_handler.py
    ├── handlers_loguru.py
    ├── handlers_more.py
    ├── helpers.py
    ├── log_manager.py
    ├── loggers_imp
    │   ├── __init__.py
    │   └── compatible_logger.py
    ├── logging_tree_helper.py
    ├── monkey_print.py
    ├── monkey_std_filter_words.py
    ├── monkey_sys_std.py
    ├── nb_log_config_default.py
    ├── root_logger.py
    ├── rotate_file_writter.py
    ├── set_nb_log_config.py
    └── simple_print.py

`````

---


## nb_log (relative dir: `nb_log`)  Included Files (total: 26 files)


- `nb_log/add_python_executable_dir_to_path_env.py`

- `nb_log/capture_warnings.py`

- `nb_log/direct_logger.py`

- `nb_log/exception_auto_log.py`

- `nb_log/file_write.py`

- `nb_log/formatters.py`

- `nb_log/frequency_control_log.py`

- `nb_log/global_except_hook.py`

- `nb_log/handlers.py`

- `nb_log/handlers_concurrent_rotating_file_handler.py`

- `nb_log/handlers_loguru.py`

- `nb_log/handlers_more.py`

- `nb_log/helpers.py`

- `nb_log/logging_tree_helper.py`

- `nb_log/log_manager.py`

- `nb_log/monkey_print.py`

- `nb_log/monkey_std_filter_words.py`

- `nb_log/monkey_sys_std.py`

- `nb_log/nb_log_config_default.py`

- `nb_log/root_logger.py`

- `nb_log/rotate_file_writter.py`

- `nb_log/set_nb_log_config.py`

- `nb_log/simple_print.py`

- `nb_log/__init__.py`

- `nb_log/loggers_imp/compatible_logger.py`

- `nb_log/loggers_imp/__init__.py`


---


--- **start of file: nb_log/add_python_executable_dir_to_path_env.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/add_python_executable_dir_to_path_env.py`

#### 📦 Imports

- `import os`
- `import sys`

#### 🔧 Public Functions (1)

- `def add_sys_executable_dir_to_path_env()`
  - *Line: 5*
  - *动态获取当前Python解释器的绝对路径所处文件夹*


---

`````python

import os
import sys

def add_sys_executable_dir_to_path_env():
    """
    动态获取当前Python解释器的绝对路径所处文件夹
    """

    #  #conda虚拟环境需要这样的pywin32在环境变量,linux用户不用管;否则必须先conda activate 虚拟环境,再运行python脚本,但这样太耗时
    # 把当前python解释器所在目录添加到环境变量,则不需要先conda activate 虚拟环境,再运行python脚本
    """
        import nb_log
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\nb_log\__init__.py", line 22, in <module>
    from nb_log import handlers
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\nb_log\handlers.py", line 25, in <module>
    from concurrent_log_handler import ConcurrentRotatingFileHandler  # 需要安装。concurrent-log-handler==0.9.1
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\concurrent_log_handler\__init__.py", line 66, in <module>
    from portalocker import LOCK_EX, lock, unlock
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\portalocker\__init__.py", line 4, in <module>
    from . import portalocker
  File "D:\ProgramData\Miniconda3\envs\py39b\lib\site-packages\portalocker\portalocker.py", line 11, in <module>
    import win32file
ImportError: DLL load failed while importing win32file: 找不到指定的模块。
    """
    # python_dir = os.path.dirname(sys.executable)
    real_python_executable = os.path.realpath(sys.executable)
    python_dir = os.path.dirname(real_python_executable)
    if os.name == 'nt':
        os.environ['path'] = python_dir + os.pathsep + os.environ['PATH']
    # print(f'{__file__} curernt python executable dir: {python_dir}')

add_sys_executable_dir_to_path_env()



`````

--- **end of file: nb_log/add_python_executable_dir_to_path_env.py** (project: nb_log) --- 

---


--- **start of file: nb_log/capture_warnings.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/capture_warnings.py`

#### 📦 Imports

- `import logging`
- `import time`
- `import warnings`
- `from collections import defaultdict`
- `import nb_log`

#### 🏛️ Classes (1)

##### 📌 `class GlobalVars`
*Line: 10*

**Class Variables (2):**
- `interval = None`
- `logger = None`

#### 🔧 Public Functions (1)

- `def capture_warnings_with_frequency_control(capture: bool = True, interval = 10)`
  - *Line: 41*
  - *对相同文件代码行的警告,使用控频来记录警告*


---

`````python
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
            file_line__ts[key] = time.time()
            s = warnings.formatwarning(message, category, filename, lineno, line)
            GlobalVars.logger.warning("%s", s)



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

`````

--- **end of file: nb_log/capture_warnings.py** (project: nb_log) --- 

---


--- **start of file: nb_log/direct_logger.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/direct_logger.py`

#### 📦 Imports

- `import logging`
- `import nb_log`

#### 🔧 Public Functions (6)

- `def debug(msg, *args, **kwargs)`
  - *Line: 45*

- `def info(msg, *args, **kwargs)`
  - *Line: 50*

- `def warning(msg, *args, **kwargs)`
  - *Line: 55*

- `def error(msg, *args, **kwargs)`
  - *Line: 60*

- `def exception(msg, *args, **kwargs)`
  - *Line: 65*

- `def critical(msg, *args, **kwargs)`
  - *Line: 70*


---

`````python
import logging

import nb_log

'''

有的笨瓜总是不能理解 logging.getLogger第一个入参name的作用和巨大好处，老是觉得需要实例化生成 logger 对象觉得麻烦，想开箱即用，那就满足这种人。
用from loguru import logger 这种日志，先不同模块或功能的日志设置不同级别，不同的模块写入不同的文件，非常麻烦不优雅。
但有的人完全不理解 日志命名空间的作用，只会抱怨nb_log的例子要他实例化不同name的logger麻烦，那就满足这种人，不用他手动实例化生成不同命名空间的logger。

import nb_log

nb_log.debug('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用debug函数，那就满足这种人')
nb_log.info('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用info函数，那就满足这种人')
nb_log.warning('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用warning函数，那就满足这种人')
nb_log.error('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用error函数，那就满足这种人')
nb_log.critical('笨瓜不想实例化多个不同name的logger,不理解logging.getLogger第一个入参name的作用和好处，想直接粗暴的调用critical函数，那就满足这种人')


loguru的用法是：
from loguru import logger
logger.debug(msg)

nb_log的用法是：
import nb_log
nb_log.debug(msg)

nb_log比loguru少了 from import那不是更简洁了吗？满足这种只知道追求简单的笨瓜。
'''

direct_logger = nb_log.LogManager('nb_log_direct', logger_cls=nb_log.CompatibleLogger).get_logger_and_add_handlers(log_filename='nb_log_direct.log')


def _convert_extra(kwargs: dict):
    """
    因为封装了原生logging的 debug info等方法，要显示实际的打印日志的文件和行号，需要把查找调用层级加大一级
    :param kwargs:
    :return:
    """
    extra = kwargs.get('extra', {})
    extra.update({"sys_getframe_n": 3})
    kwargs['extra'] = extra


def debug(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.error(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.exception(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    _convert_extra(kwargs)
    direct_logger.critical(msg, *args, **kwargs)

`````

--- **end of file: nb_log/direct_logger.py** (project: nb_log) --- 

---


--- **start of file: nb_log/exception_auto_log.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/exception_auto_log.py`

#### 📦 Imports

- `import time`
- `import logging`
- `import nb_log`
- `from nb_log import CompatibleLogger`

#### 🏛️ Classes (1)

##### 📌 `class LogException(Exception)`
*Line: 8*

**Docstring:**
`````
自动记录日志的异常，抛出异常不需要单独再写日志
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, err_msg)`
  - **Parameters:**
    - `self`
    - `err_msg`

**Class Variables (2):**
- `logger: logging.Logger = None`
- `is_record_log: bool = True`


---

`````python
import time

import logging
import nb_log
from nb_log import CompatibleLogger


class LogException(Exception):
    """
    自动记录日志的异常，抛出异常不需要单独再写日志
    """
    logger: logging.Logger = None
    is_record_log: bool = True

    def __init__(self, err_msg, *, logger: logging.Logger = None, is_record_log: bool = True):  # real signature unknown
        logger = logger or self.__class__.logger
        self.err_msg = err_msg
        if logger and (is_record_log or self.__class__.is_record_log):
            logger.error(self.err_msg, extra={'sys_getframe_n': 3})

    def __str__(self):
        return str(self.err_msg)


if __name__ == '__main__':
    loggerx = nb_log.LogManager('log_exc', logger_cls=CompatibleLogger).get_logger_and_add_handlers(log_filename='log_exc.log')

    # try:
    #     raise LogException(['cccc', 222], logger=loggerx)
    # except Exception as e:
    #     print(e)
    # try:
    #     raise LogException('cccc', logger=loggerx)
    # except Exception as e:
    #     loggerx.exception(e)

    # print('aaaaaaaaaaaaaaaa')
    time.sleep(1)
    raise LogException(['cccc', 222], logger=loggerx)  #

    print('ok')

`````

--- **end of file: nb_log/exception_auto_log.py** (project: nb_log) --- 

---


--- **start of file: nb_log/file_write.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/file_write.py`

#### 📦 Imports

- `import threading`
- `from functools import wraps`
- `from pathlib import Path`
- `from nb_log import nb_log_config_default`
- `import time`
- `from chained_mode_time_tool import DatetimeConverter`
- `from nb_log.simple_print import sprint`

#### 🏛️ Classes (3)

##### 📌 `class FileWritter`
*Line: 28*

**🔧 Constructor (`__init__`):**
- `def __init__(self, file_name: str, log_path = nb_log_config_default.LOG_PATH)`
  - **Parameters:**
    - `self`
    - `file_name: str`
    - `log_path = nb_log_config_default.LOG_PATH`

**Public Methods (1):**
- `def write_2_file(self, msg)`

**Class Variables (2):**
- `_lock = threading.Lock()`
- `need_write_2_file = True`

##### 📌 `class PrintFileWritter(FileWritter)`
*Line: 73*

**Class Variables (2):**
- `_lock = threading.Lock()`
- `need_write_2_file = False if nb_log_config_default.PRINT_WRTIE_FILE_NAME in (None, '') else True`

##### 📌 `class StdFileWritter(FileWritter)`
*Line: 78*

**Class Variables (2):**
- `_lock = threading.Lock()`
- `need_write_2_file = False if nb_log_config_default.SYS_STD_FILE_NAME in (None, '') else True`

#### 🔧 Public Functions (1)

- `def singleton(cls)`
  - *Line: 10*
  - *单例模式装饰器,新加入线程锁，更牢固的单例模式，主要解决多线程如100线程同时实例化情况下可能会出现三例四例的情况,实测。*


---

`````python
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
    fw = FileWritter('test_file3', '/test_dir2')
    t1 = time.time()
    for i in range(10000):
        fw.write_2_file(''' 11:18:13  "D:\codes\nb_log\tests\test_use_curretn_dir_config\test_s_print2.py:9"  <module>  2023-07-05 10:48:35 - lalala - "D:/codes/funboost/test_frame/test_nb_log/log_example.py:15" - <module> - ERROR - 粉红色说明代码有错误。 粉红色说明代码有错误。 粉红色说明代码有错误。 粉红色说明代码有错误。
  ''')
    print(time.time()-t1)
`````

--- **end of file: nb_log/file_write.py** (project: nb_log) --- 

---


--- **start of file: nb_log/formatters.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/formatters.py`

#### 📦 Imports

- `import logging`
- `import typing`
- `from logging import Formatter`
- `from logging import LogRecord`

#### 🏛️ Classes (1)

##### 📌 `class ContextFormatter(Formatter)`
*Line: 6*

**🔧 Constructor (`__init__`):**
- `def __init__(self, *args, **kwargs)`
  - **Parameters:**
    - `self`
    - `*args`
    - `**kwargs`

**Public Methods (1):**
- `def formatMessage(self, record: LogRecord)`

#### 🔧 Public Functions (1)

- `def f()`
  - *Line: 20*


---

`````python
import logging
import typing
from logging import Formatter, LogRecord


class ContextFormatter(Formatter):
    def __init__(self, *args, get_context_field_fun: typing.Callable = None, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.get_context_field_fun = get_context_field_fun

    def formatMessage(self, record: LogRecord):
        context_id = ''
        if self.get_context_field_fun:
            context_id = self.get_context_field_fun()
        setattr(record, 'context_id', context_id)
        return self._style.format(record)


if __name__ == '__main__':
    def f():
        return 'aaaaaa6666'


    logger = logging.getLogger('abcd')
    sh = logging.StreamHandler()
    formatter = ContextFormatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(context_id)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
        "%Y-%m-%d %H:%M:%S", get_context_field_fun=None)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    logger.info('哈哈哈哈')

`````

--- **end of file: nb_log/formatters.py** (project: nb_log) --- 

---


--- **start of file: nb_log/frequency_control_log.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/frequency_control_log.py`

#### 📦 Imports

- `import copy`
- `import logging`
- `import sys`
- `import time`
- `import typing`
- `from nb_libs.sys_frame_uitils import EasyFrame`

#### 🏛️ Classes (1)

##### 📌 `class FrequencyControlLog`
*Line: 10*

**🔧 Constructor (`__init__`):**
- `def __init__(self, logger: logging.Logger, interval = 10)`
  - **Parameters:**
    - `self`
    - `logger: logging.Logger`
    - `interval = 10`

**Properties (6):**
- `@property log -> logging.Logger.log`
- `@property debug -> typing.Callable`
- `@property info -> logging.Logger.info`
- `@property warning -> logging.Logger.warning`
- `@property error -> logging.Logger.error`
- `@property critical -> logging.Logger.critical`

**Class Variables (1):**
- `file_line__ts_map = dict()`


---

`````python
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

`````

--- **end of file: nb_log/frequency_control_log.py** (project: nb_log) --- 

---


--- **start of file: nb_log/global_except_hook.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/global_except_hook.py`

#### 📦 Imports

- `import traceback`
- `import sys`
- `import logging`
- `import nb_log`

#### 🔧 Public Functions (2)

- `def global_except_hook(exctype, value, tracebackx)`
  - *Line: 9*

- `def test_exception()`
  - *Line: 23*


---

`````python
import traceback

import sys
import logging
import nb_log


logger = nb_log.get_logger('global_except_hook',log_filename='global_except_hook.log')
def global_except_hook(exctype, value, tracebackx):
    # 输出异常信息到日志
    # print(exctype)
    # print(value)
    # print(traceback.format_tb(tracebackx))
    logger.error('Unhandled exception:', exc_info=(exctype, value, tracebackx))

# 设置全局异常钩子
sys.excepthook = global_except_hook



if __name__ == '__main__':
    # 测试异常
    def test_exception():
        try:
            raise ValueError('Test exception')
        except Exception as e:
            pass
            raise OSError('aaaa32') from e


    # 触发异常
    print(ValueError.__name__)
    test_exception()
`````

--- **end of file: nb_log/global_except_hook.py** (project: nb_log) --- 

---


--- **start of file: nb_log/handlers.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/handlers.py`

#### 📦 Imports

- `import atexit`
- `import copy`
- `import multiprocessing`
- `import queue`
- `import re`
- `import sys`
- `import os`
- `import threading`
- `import traceback`
- `import socket`
- `import datetime`
- `import json`
- `import time`
- `import typing`
- `from collections import OrderedDict`
- `from pathlib import Path`
- `from queue import Queue`
- `from queue import Empty`
- `from threading import Lock`
- `from threading import Thread`
- `import requests`
- `import logging`
- `from logging import handlers`
- `from logging.handlers import WatchedFileHandler`
- `from nb_filelock import FileLock`
- `from pythonjsonlogger.jsonlogger import JsonFormatter`
- `from nb_log import nb_log_config_default`
- `from nb_log.monkey_print import nb_print`
- `from nb_log.rotate_file_writter import OsFileWritter`
- `from threading import Thread`
- `from threading import Thread`
- `import smtplib`
- `from email.message import EmailMessage`
- `import email.utils`
- `from nb_filelock import FileLock`

#### 🏛️ Classes (7)

##### 📌 `class ColorHandler(logging.Handler)`
*Line: 55*

**Docstring:**
`````
根据日志严重级别，显示成五彩控制台日志。
强烈建议使用pycharm的 monokai主题颜色，这样日志的颜色符合常规的交通信号灯颜色指示，色彩也非常饱和鲜艳。
设置方式为 打开pycharm的settings -> Editor -> Color Scheme -> Console Font 选择monokai
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, stream = None)`
  - **Docstring:**
  `````
  Initialize the handler.
  
  If stream is not specified, sys.stderr is used.
  `````
  - **Parameters:**
    - `self`
    - `stream = None`

**Public Methods (2):**
- `def flush(self)`
  - *Flushes the stream.*
- `def emit(self, record: logging.LogRecord)`
  - **Docstring:**
  `````
  Emit a record.
  
  If a formatter is specified, it is used to format the record.
  The record is then written to the stream with a trailing newline.  If
  exception information is present, it is formatted using
  traceback.print_exception and appended to the stream.  If the stream
  has an 'encoding' attribute, it is used to determine how to do the
  output to the stream.
  `````

**Class Variables (3):**
- `terminator = '\r\n' if os_name == 'nt' else '\n'`
- `bule = 96 if os_name == 'nt' else 36`
- `yellow = 93 if os_name == 'nt' else 33`

##### 📌 `class CompatibleSMTPSSLHandler(handlers.SMTPHandler)`
*Line: 278*

**Docstring:**
`````
官方的SMTPHandler不支持SMTP_SSL的邮箱，这个可以两个都支持,并且支持邮件发送频率限制
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, mailhost, fromaddr, toaddrs: tuple, subject, credentials = None, secure = None, timeout = 5.0, is_use_ssl = True, mail_time_interval = 0)`
  - **Docstring:**
  `````
  :param mailhost:
  :param fromaddr:
  :param toaddrs:
  :param subject:
  :param credentials:
  :param secure:
  :param timeout:
  :param is_use_ssl:
  :param mail_time_interval: 发邮件的时间间隔，可以控制日志邮件的发送频率，为0不进行频率限制控制，如果为60，代表1分钟内最多发送一次邮件
  `````
  - **Parameters:**
    - `self`
    - `mailhost`
    - `fromaddr`
    - `toaddrs: tuple`
    - `subject`
    - `credentials = None`
    - `secure = None`
    - `timeout = 5.0`
    - `is_use_ssl = True`
    - `mail_time_interval = 0`

**Public Methods (2):**
- `def emit0(self, record: logging.LogRecord)`
  - *不用这个判断内容*
- `def emit(self, record: logging.LogRecord)`
  - **Docstring:**
  `````
  Emit a record.
  
  Format the record and send it to the specified addressees.
  `````

##### 📌 `class DingTalkHandler(logging.Handler)`
*Line: 374*

**🔧 Constructor (`__init__`):**
- `def __init__(self, ding_talk_token = None, time_interval = 60)`
  - **Parameters:**
    - `self`
    - `ding_talk_token = None`
    - `time_interval = 60`

**Public Methods (1):**
- `def emit(self, record)`

**Class Variables (1):**
- `_lock_for_remove_handlers = Lock()`

##### 📌 `class ConcurrentDayRotatingFileHandlerWin(logging.Handler)`
*Line: 426*

**Docstring:**
`````
这个多进程按时间切片安全的。
官方的 TimedRotatingFileHandler 在多进程下疯狂报错，
不信的话可以试试官方 TimedRotatingFileHandler 多进程写入文件日志，设置成每秒换一个新的文件写(主要是按天来切割要耽误很长的时间才能观察错误)
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, file_name: str, file_path: str, back_count = None)`
  - **Parameters:**
    - `self`
    - `file_name: str`
    - `file_path: str`
    - `back_count = None`

**Public Methods (1):**
- `def emit(self, record: logging.LogRecord)`
  - **Docstring:**
  `````
  emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
  :param record:
  :return:
  `````

**Class Variables (3):**
- `file_handler_list = []`
- `has_start_emit_all_file_handler_process_id_set = set()`
- `__lock_for_rotate = Lock()`

##### 📌 `class ConcurrentDayRotatingFileHandlerLinux(logging.Handler)`
*Line: 538*

**🔧 Constructor (`__init__`):**
- `def __init__(self, file_name: str, file_path: str, back_count = None)`
  - **Parameters:**
    - `self`
    - `file_name: str`
    - `file_path: str`
    - `back_count = None`

**Public Methods (2):**
- `def emit(self, record: logging.LogRecord)`
  - **Docstring:**
  `````
  emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
  :param record:
  :return:
  `````
- `def close(self)`

##### 📌 `class _ConcurrentSecondRotatingFileHandlerLinux(logging.Handler)`
*Line: 628*

**Docstring:**
`````
按秒切割的多进程安全文件日志，方便测试验证
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, file_name: str, file_path: str, back_count = None)`
  - **Parameters:**
    - `self`
    - `file_name: str`
    - `file_path: str`
    - `back_count = None`

**Public Methods (1):**
- `def emit(self, record: logging.LogRecord)`
  - **Docstring:**
  `````
  emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
  :param record:
  :return:
  `````

##### 📌 `class BothDayAndSizeRotatingFileHandler(logging.Handler)`
*Line: 722*

**Docstring:**
`````
自己从头开发的按照时间和大小切割
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, file_name: typing.Optional[str], log_path = '/pythonlogs', max_bytes = 1000 * 1000 * 1000, back_count = 10)`
  - **Parameters:**
    - `self`
    - `file_name: typing.Optional[str]`
    - `log_path = '/pythonlogs'`
    - `max_bytes = 1000 * 1000 * 1000`
    - `back_count = 10`

**Public Methods (1):**
- `def emit(self, record: logging.LogRecord) -> None`

#### 🔧 Public Functions (1)

- `def formatMessage(self, record: logging.LogRecord)`
  - *Line: 42*


---

`````python
# noinspection PyMissingOrEmptyDocstring
import atexit
import copy
import multiprocessing
import queue
import re
import sys
import os
import threading
import traceback
import socket
import datetime
import json
import time
import typing

from collections import OrderedDict
from pathlib import Path
from queue import Queue, Empty

from threading import Lock, Thread
import requests
import logging
from logging import handlers

# noinspection PyUnresolvedReferences
from logging.handlers import WatchedFileHandler
# noinspection PyPackageRequirements
from nb_filelock import FileLock
from pythonjsonlogger.jsonlogger import JsonFormatter
from nb_log import nb_log_config_default
from nb_log.monkey_print import nb_print
from nb_log.rotate_file_writter import OsFileWritter

very_nb_print = nb_print
os_name = os.name

host_name = socket.gethostname()


# noinspection PyPep8Naming
def formatMessage(self, record: logging.LogRecord):
    # print(record.__dict__)
    if hasattr(record, 'for_segmentation_color'):
        # del record.for_segmentation_color
        # del record.msg
        record.message = ''
    # print(record.__dict__)
    return self._style.format(record)


# logging.Formatter.formatMessage = formatMessage


class ColorHandler(logging.Handler):
    """
    根据日志严重级别，显示成五彩控制台日志。
    强烈建议使用pycharm的 monokai主题颜色，这样日志的颜色符合常规的交通信号灯颜色指示，色彩也非常饱和鲜艳。
    设置方式为 打开pycharm的settings -> Editor -> Color Scheme -> Console Font 选择monokai
    """

    terminator = '\r\n' if os_name == 'nt' else '\n'
    bule = 96 if os_name == 'nt' else 36
    yellow = 93 if os_name == 'nt' else 33

    def __init__(self, stream=None, ):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        logging.Handler.__init__(self)
        if stream is None:
            stream = sys.stdout  # stderr无彩。
        self.stream = stream
        self._display_method = 7 if os_name == 'posix' else 0

    def flush(self):
        """
        Flushes the stream.
        """
        self.acquire()
        try:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
        finally:
            self.release()

    def __build_color_msg_with_backgroud_color000(self, record_level, assist_msg, effective_information_msg):

        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{assist_msg}\033[0m \033[0;37;42m{effective_information_msg}\033[0m'  # 绿色
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{assist_msg}\033[0m \033[0;37;46m{effective_information_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{assist_msg}\033[0m \033[0;37;43m{effective_information_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;35m{assist_msg}\033[0m \033[0;37;45m{effective_information_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
            msg_color = f'\033[0;31m{assist_msg}\033[0m \033[0;37;41m{effective_information_msg}\033[0m'
        else:
            msg_color = f'{assist_msg}  {effective_information_msg}'
        return msg_color

    @staticmethod
    def __build_color_msg_with_no_backgroud_color000(record_level, assist_msg, effective_information_msg):

        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{assist_msg} {effective_information_msg}\033[0m'  # 绿色
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;35m{assist_msg} {effective_information_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
            msg_color = f'\033[0;31m{assist_msg} {effective_information_msg}\033[0m'
        else:
            msg_color = f'{assist_msg}  {effective_information_msg}'
        return msg_color

    def __build_color_msg_with_backgroud_color(self, record_level, record_copy: logging.LogRecord, ):
        background_color = ''
        complete_color = ''
        if record_level == 10:
            background_color = f'[0;30;42m'
            complete_color = f'[0;32m'
        elif record_level == 20:
            background_color = f'[0;30;46m'
            complete_color = f'[0;36m'
        elif record_level == 30:
            background_color = f'[0;30;43m'
            complete_color = f'[0;33m'
        elif record_level == 40:
            background_color = f'[0;37;45m'
            complete_color = f'[0;35m'
        elif record_level == 50:
            background_color = f'[0;37;41m'
            complete_color = f'[0;31m'
        record_copy.msg = f'\033{background_color}{record_copy.msg}\033[0m'
        msg_color_without = self.format(record_copy)
        # print(repr(msg_color))
        if isinstance(self.formatter, JsonFormatter) and background_color:  # json会把/033 转义成\u001b,导致颜色显示不出来。
            msg_color_without = msg_color_without.replace(rf'\u001b{background_color}', f'\033{background_color}')
            msg_color_without = msg_color_without.replace(r'\u001b[0m', f'\033[0m\033{complete_color}')
        msg_color = f'\033{complete_color}{msg_color_without}\033[0m'
        # print(repr(msg_color))
        return msg_color


    def __build_color_msg_with_backgroud_color3333(self, record_level, record_copy: logging.LogRecord, ):
        background_color = ''
        complete_color = ''
        if record_level == 10:
            background_color = f'[0;30;42m'
            complete_color = f'[0;32m'
        elif record_level == 20:
            background_color = f'[0;30;46m'
            complete_color = f'[0;36m'
        elif record_level == 30:
            background_color = f'[0;30;43m'
            complete_color = f'[0;33m'
        elif record_level == 40:
            background_color = f'[0;37;45m'
            complete_color = f'[0;35m'
        elif record_level == 50:
            background_color = f'[0;37;41m'
            complete_color = f'[0;31m'
        record_copy.msg = f'\033{complete_color}{record_copy.msg}\033[0m'
        msg_color_without = self.format(record_copy)
        # print(repr(msg_color))
        if isinstance(self.formatter, JsonFormatter) and background_color:  # json会把/033 转义成\u001b,导致颜色显示不出来。
            msg_color_without = msg_color_without.replace(rf'\u001b{background_color}', f'\033{background_color}')
            msg_color_without = msg_color_without.replace(r'\u001b[0m', f'\033[0m\033{complete_color}')
        # msg_color = f'\033{complete_color}{msg_color_without}\033[0m'
        msg_color = f'\033{background_color}{msg_color_without}\033[0m'
        # print(repr(msg_color))
        return msg_color

    def __build_color_msg_with_no_backgroud_color(self, record_level, record_copy: logging.LogRecord, ):
        complete_msg = self.format(record_copy)
        if record_level == 10:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{complete_msg}\033[0m'  # 绿色
        elif record_level == 20:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{complete_msg}\033[0m'
        elif record_level == 30:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{complete_msg}\033[0m'
        elif record_level == 40:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;35m{complete_msg}\033[0m'
        elif record_level == 50:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
            msg_color = f'\033[0;31m{complete_msg}\033[0m'
        else:
            msg_color = f'{complete_msg}'
        return msg_color

    def emit(self, record: logging.LogRecord):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        # noinspection PyBroadException
        try:
            # very_nb_print(record)
            # record.message = record.getMessage()
            # effective_information_msg = record.getMessage()  # 不能用msg字段，例如有的包的日志格式化还有其他字段
            # record_copy = copy.copy(record)  # copy是因为，不要因为要屏幕彩色日志而影响例如文件日志 叮叮日志等其他handler的格式。
            # record_copy.for_segmentation_color = '彩色分段标志属性而已'
            # del record_copy.msg
            # assist_msg = self.format(record_copy)
            # print(f'**  {assist_msg}  ** ')
            stream = self.stream
            # print(assist_msg)
            # print(effective_information_msg)
            # record.raw_no_color_msg = record.msg
            if nb_log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
                msg_color = self.__build_color_msg_with_backgroud_color(record.levelno, copy.copy(record))
            else:
                msg_color = self.__build_color_msg_with_no_backgroud_color(record.levelno, copy.copy(record))
            # stream.write(msg_color)
            # stream.write(self.terminator)
            # self.flush()
            stream.write(msg_color + self.terminator)
            # self.flush()
        except Exception as e:
            very_nb_print(e)
            very_nb_print(traceback.format_exc())
            # self.handleError(record)

    @staticmethod
    def __spilt_msg(log_level, msg: str):
        split_text = '- 级别 -'
        if log_level == logging.DEBUG:
            split_text = '- DEBUG -'
        elif log_level == logging.INFO:
            split_text = '- INFO -'
        elif log_level == logging.WARNING:
            split_text = '- WARNING -'
        elif log_level == 40:
            split_text = '- ERROR -'
        elif log_level == 50:
            split_text = '- CRITICAL -'
        msg_split = msg.split(split_text, maxsplit=1)
        return msg_split[0] + split_text, msg_split[-1]

    def __repr__(self):
        level = logging.getLevelName(self.level)
        name = getattr(self.stream, 'name', '')
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)



class CompatibleSMTPSSLHandler(handlers.SMTPHandler):
    """
    官方的SMTPHandler不支持SMTP_SSL的邮箱，这个可以两个都支持,并且支持邮件发送频率限制
    """

    def __init__(self, mailhost, fromaddr, toaddrs: tuple, subject,
                 credentials=None, secure=None, timeout=5.0, is_use_ssl=True, mail_time_interval=0):
        """

        :param mailhost:
        :param fromaddr:
        :param toaddrs:
        :param subject:
        :param credentials:
        :param secure:
        :param timeout:
        :param is_use_ssl:
        :param mail_time_interval: 发邮件的时间间隔，可以控制日志邮件的发送频率，为0不进行频率限制控制，如果为60，代表1分钟内最多发送一次邮件
        """
        # noinspection PyCompatibility
        # very_nb_print(credentials)
        # noinspection PyTypeChecker
        super().__init__(mailhost, fromaddr, toaddrs, subject,
                         credentials, secure, timeout)
        self._is_use_ssl = is_use_ssl
        self._current_time = 0
        self._time_interval = 3600 if mail_time_interval < 3600 else mail_time_interval  # 60分钟发一次群发邮件，以后用钉钉代替邮件，邮件频率限制的太死了。
        self._msg_map = dict()  # 是一个内容为键时间为值得映射
        self._lock = Lock()

    def emit0(self, record: logging.LogRecord):
        """
        不用这个判断内容
        """
        from threading import Thread
        if sys.getsizeof(self._msg_map) > 10 * 1000 * 1000:
            self._msg_map.clear()
        if record.msg not in self._msg_map or time.time() - self._msg_map[record.msg] > self._time_interval:
            self._msg_map[record.msg] = time.time()
            # print('发送邮件成功')
            Thread(target=self.__emit, args=(record,)).start()
        else:
            very_nb_print(f' 邮件发送太频繁间隔不足60分钟，此次不发送这个邮件内容： {record.msg}    ')

    def emit(self, record: logging.LogRecord):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        from threading import Thread
        with self._lock:
            if time.time() - self._current_time > self._time_interval:
                self._current_time = time.time()
                Thread(target=self.__emit, args=(record,)).start()
            else:
                # very_nb_print(f' 邮件发送太频繁间隔不足60分钟，此次不发送这个邮件内容： {record.msg}     ')
                very_nb_print(f' 邮件发送太频繁间隔不足 {self._time_interval}  秒 ，此次不发送这个邮件内容： {record.msg}     ')

    # noinspection PyUnresolvedReferences
    def __emit(self, record):
        # noinspection PyBroadException
        try:
            import smtplib
            from email.message import EmailMessage
            import email.utils
            t_start = time.time()
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self.timeout) if self._is_use_ssl else smtplib.SMTP(
                self.mailhost, port, timeout=self.timeout)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.send_message(msg)
            smtp.quit()
            # noinspection PyPep8
            very_nb_print(
                f'发送邮件给 {self.toaddrs} 成功，'
                f'用时{round(time.time() - t_start, 2)} ,发送的内容是--> {record.msg}                    \033[0;35m!!!请去邮箱检查，可能在垃圾邮件中\033[0m')
        except Exception as e:
            # self.handleError(record)
            very_nb_print(
                f'[log_manager.py]   {time.strftime("%H:%M:%S", time.localtime())}  \033[0;31m !!!!!! 邮件发送失败,原因是： {e} \033[0m')


class DingTalkHandler(logging.Handler):
    _lock_for_remove_handlers = Lock()

    def __init__(self, ding_talk_token=None, time_interval=60):
        super().__init__()
        self.ding_talk_token = ding_talk_token
        self._ding_talk_url = f'https://oapi.dingtalk.com/robot/send?access_token={ding_talk_token}'
        self._current_time = 0
        self._time_interval = time_interval  # 最好别频繁发。
        self._lock = Lock()

    def emit(self, record):
        # from threading import Thread
        with self._lock:
            if time.time() - self._current_time > self._time_interval:
                # very_nb_print(self._current_time)
                self._current_time = time.time()
                self.__emit(record)
                # Thread(target=self.__emit, args=(record,)).start()

            else:
                very_nb_print(f' 此次离上次发送钉钉消息时间间隔不足 {self._time_interval} 秒，此次不发送这个钉钉内容： {record.msg}    ')

    def __emit(self, record):
        message = self.format(record)
        very_nb_print(message)
        data = {"msgtype": "text", "text": {"content": message, "title": '这里的标题能起作用吗？？'}}
        try:
            self._remove_urllib_hanlder()  # 因为钉钉发送也是使用requests实现的，如果requests调用的urllib3命名空间也加上了钉钉日志，将会造成循环，程序卡住。一般情况是在根日志加了钉钉handler。
            resp = requests.post(self._ding_talk_url, json=data, timeout=(5, 5))
            very_nb_print(f'钉钉返回 ： {resp.text}')
        except requests.RequestException as e:
            very_nb_print(f"发送消息给钉钉机器人失败 {e}")

    def __repr__(self):
        level = logging.getLevelName(self.level)
        return '<%s (%s)>' % (self.__class__.__name__, level) + ' dingtalk token is ' + self.ding_talk_token

    @classmethod
    def _remove_urllib_hanlder(cls):
        for name in ['root', 'urllib3', 'requests']:
            cls.__remove_urllib_hanlder_by_name(name)

    @classmethod
    def __remove_urllib_hanlder_by_name(cls, logger_name):
        with cls._lock_for_remove_handlers:
            for index, hdlr in enumerate(logging.getLogger(logger_name).handlers):
                if 'DingTalkHandler' in str(hdlr):
                    logging.getLogger(logger_name).handlers.pop(index)


# noinspection PyPep8Naming
class ConcurrentDayRotatingFileHandlerWin(logging.Handler):
    """
    这个多进程按时间切片安全的。
    官方的 TimedRotatingFileHandler 在多进程下疯狂报错，
    不信的话可以试试官方 TimedRotatingFileHandler 多进程写入文件日志，设置成每秒换一个新的文件写(主要是按天来切割要耽误很长的时间才能观察错误)
    """
    file_handler_list = []
    has_start_emit_all_file_handler_process_id_set = set()  # 这个linux和windwos都兼容，windwos是多进程每个进程的变量has_start_emit_all_file_handler是独立的。linux是共享的。
    __lock_for_rotate = Lock()

    @classmethod
    def _emit_all_file_handler(cls):
        while True:
            # print(os.getpid())
            for hr in cls.file_handler_list:
                # very_nb_print(hr.buffer_msgs_queue.qsize())
                # noinspection PyProtectedMember
                hr._write_to_file()
            time.sleep(1)  # 每隔一秒钟批量写入一次，性能好了很多。

    @classmethod
    def _start_emit_all_file_handler(cls):
        pass
        Thread(target=cls._emit_all_file_handler, daemon=True).start()

    # noinspection PyMissingConstructor
    def __init__(self, file_name: str, file_path: str, back_count=None):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count or nb_log_config_default.LOG_FILE_BACKUP_COUNT
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = 0

        self.buffer_msgs_queue = queue.Queue()
        atexit.register(self._write_to_file)  # 如果程序属于立马就能结束的，需要在程序结束前执行这个钩子，防止不到最后一秒的日志没记录到。
        self.file_handler_list.append(self)
        if os.getpid() not in self.has_start_emit_all_file_handler_process_id_set:
            self._start_emit_all_file_handler()
            self.__class__.has_start_emit_all_file_handler_process_id_set.add(os.getpid())

    def emit(self, record: logging.LogRecord):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.buffer_msgs_queue.put(msg)
        except Exception:
            self.handleError(record)

    def _write_to_file(self):  # 也可以重写 close方法，来处理末尾。
        buffer_msgs = ''
        while True:
            # print(self.buffer_msgs_queue.qsize())
            try:
                msg = self.buffer_msgs_queue.get(block=False)
                buffer_msgs += msg + '\n'
                if len(buffer_msgs) > 1000 * 1000 * 10:
                    pass
                    break
            except queue.Empty:
                break
        if buffer_msgs:
            from nb_filelock import FileLock
            with FileLock(self.file_path / Path(f'_delete_{self.file_name}.lock')):
                time_str = time.strftime('%Y-%m-%d')
                # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
                new_file_name = self.file_name + '.' + time_str
                path_obj = Path(self.file_path) / Path(new_file_name)
                path_obj.touch(exist_ok=True)
                with path_obj.open(mode='a', encoding='utf-8') as f:
                    f.write(buffer_msgs)
                    f.flush()
                if time.time() - self._last_delete_time > 60:
                    self._find_and_delete_files()
                    self._last_delete_time = time.time()

    def _find_and_delete_files(self):
        """
        这一段命名不规范是复制原来的官方旧代码。
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName = self.file_path
        baseName = self.file_name
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # print(fileName, prefix,suffix)
                if self.extMatch.match(suffix) or self.extMatch2.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        # print(result)
        for r in result:
            Path(r).unlink()


# noinspection PyPep8Naming
class ConcurrentDayRotatingFileHandlerLinux(logging.Handler):
    def __init__(self, file_name: str, file_path: str, back_count=None):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count or nb_log_config_default.LOG_FILE_BACKUP_COUNT
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = time.time()

        time_str = time.strftime('%Y-%m-%d')
        # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
        new_file_name = self.file_name + '.' + time_str
        path_obj = Path(self.file_path) / Path(new_file_name)
        path_obj.touch(exist_ok=True)
        self.fp = open(path_obj, 'a', encoding='utf-8')
        self.time_str = time_str
        self._lock = multiprocessing.Lock()

    def _get_fp(self):
        with self._lock:
            time_str = time.strftime('%Y-%m-%d')
            # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
            if time_str != self.time_str:
                try:
                    self.fp.close()
                except Exception as e:
                    print(e)
                new_file_name = self.file_name + '.' + time_str
                path_obj = Path(self.file_path) / Path(new_file_name)
                path_obj.touch(exist_ok=True)
                self.fp = open(path_obj, 'a', encoding='utf-8')

    def emit(self, record: logging.LogRecord):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.fp.write(msg + '\n')
            self.fp.flush()  # 需要flush才能及时写入。重写close可以写入程序结束前的缓冲。
        except Exception as e:
            print(e)
            self.handleError(record)
        if time.time() - self._last_delete_time > 60:
            self._get_fp()
            self._find_and_delete_files()
            self._last_delete_time = time.time()

    def close(self):
        with self._lock:
            try:
                self.fp.flush()
                self.fp.close()
            except Exception as e:
                print(e)

    def _find_and_delete_files(self):
        """
        这一段命名不规范是复制原来的官方旧代码。
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName = self.file_path
        baseName = self.file_name
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # print(fileName, prefix,suffix)
                if self.extMatch.match(suffix) or self.extMatch2.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        # print(result)
        for r in result:
            Path(r).unlink()


# noinspection PyPep8Naming
class _ConcurrentSecondRotatingFileHandlerLinux(logging.Handler):
    """ 按秒切割的多进程安全文件日志，方便测试验证"""

    def __init__(self, file_name: str, file_path: str, back_count=None):
        super().__init__()
        self.file_name = file_name
        self.file_path = file_path
        self.backupCount = back_count or nb_log_config_default.LOG_FILE_BACKUP_COUNT
        self.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self.extMatch2 = re.compile(r"^\d{2}-\d{2}-\d{2}(\.\w+)?$", re.ASCII)
        self._last_delete_time = 0

        time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
        new_file_name = self.file_name + '.' + time_str
        path_obj = Path(self.file_path) / Path(new_file_name)
        path_obj.touch(exist_ok=True)
        self.fp = open(path_obj, 'a', encoding='utf-8')
        self.time_str = time_str
        self._lock = multiprocessing.Lock()

    def _get_fp(self):
        with self._lock:
            time_str = time.strftime('%H-%M-%S')
            # time_str = time.strftime('%H-%M-%S')  # 方便测试用的，方便观察。
            if time_str != self.time_str:
                try:
                    pass
                    # self.fp.close()
                except Exception as e:
                    print(e)
                new_file_name = self.file_name + '.' + time_str
                path_obj = Path(self.file_path) / Path(new_file_name)
                path_obj.touch(exist_ok=True)
                self.fp = open(path_obj, 'a', encoding='utf-8')

    def emit(self, record: logging.LogRecord):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            if time.time() - self._last_delete_time > 0.5:
                self._get_fp()
                self._find_and_delete_files()
                self._last_delete_time = time.time()
            self.fp.write(msg + '\n')
        except Exception as e:
            print(e)
            self.handleError(record)

    def _find_and_delete_files(self):
        """
        这一段命名不规范是复制原来的官方旧代码。
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName = self.file_path
        baseName = self.file_name
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # print(fileName, prefix,suffix)
                if self.extMatch.match(suffix) or self.extMatch2.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        # print(result)
        for r in result:
            try:
                Path(r).unlink()
                print(f'删除成功 {r}')
            except (PermissionError, FileNotFoundError) as e:
                print(e)


ConcurrentDayRotatingFileHandler = ConcurrentDayRotatingFileHandlerWin if os_name == 'nt' else ConcurrentDayRotatingFileHandlerLinux


# ConcurrentDayRotatingFileHandler = ConcurrentSecondRotatingFileHandlerLinux
#
# print(ConcurrentDayRotatingFileHandler)


class BothDayAndSizeRotatingFileHandler(logging.Handler):
    """
    自己从头开发的按照时间和大小切割
    """

    def __init__(self, file_name: typing.Optional[str], log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000, back_count=10):
        super().__init__()
        self.baseFilename = Path(log_path).joinpath(file_name).as_posix()
        self.os_file_writter = OsFileWritter(file_name=file_name, log_path=log_path, max_bytes=max_bytes, back_count=back_count)

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.os_file_writter.write_2_file(msg + '\n')

    def __repr__(self):
        level = logging.getLevelName(self.level)
        return '<%s %s (%s)>' % (self.__class__.__name__, self.baseFilename, level)

`````

--- **end of file: nb_log/handlers.py** (project: nb_log) --- 

---


--- **start of file: nb_log/handlers_concurrent_rotating_file_handler.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/handlers_concurrent_rotating_file_handler.py`

#### 📦 Imports

- `from concurrent_log_handler import ConcurrentRotatingFileHandler`
- `import time`
- `from threading import Thread`
- `import atexit`
- `import queue`
- `from queue import Empty`
- `from queue import SimpleQueue`

#### 🏛️ Classes (1)

##### 📌 `class ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(ConcurrentRotatingFileHandler)`
*Line: 8*

**Docstring:**
`````
ConcurrentRotatingFileHandler 解决了多进程下文件切片问题，但频繁操作文件锁，带来程序性能巨大下降。
反复测试极限日志写入频次，在windows上比不切片的写入性能降低100倍。在linux上比不切片性能降低10倍。多进程切片文件锁在windows使用pywin32，在linux上还是要fcntl实现。
所以此类使用缓存1秒钟内的日志为一个长字符串再插入，大幅度地降低了文件加锁和解锁的次数，速度比不做多进程安全切片的文件写入速度更快。
主动触发写入文件。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, *args, **kwargs)`
  - **Parameters:**
    - `self`
    - `*args`
    - `**kwargs`

**Public Methods (3):**
- `def start_emit_all_file_handler(cls)` `classmethod`
- `def emit(self, record)`
  - **Docstring:**
  `````
  emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
  :param record:
  :return:
  `````
- `def rollover_and_do_write(self)`

**Class Variables (2):**
- `file_handler_list = []`
- `has_start_emit_all_file_handler = False`


---

`````python
from concurrent_log_handler import ConcurrentRotatingFileHandler  # 需要安装。concurrent-log-handler==0.9.1
import time
from threading import Thread
import atexit
import queue
from queue import Empty, SimpleQueue

class ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(ConcurrentRotatingFileHandler):
    """
    ConcurrentRotatingFileHandler 解决了多进程下文件切片问题，但频繁操作文件锁，带来程序性能巨大下降。
    反复测试极限日志写入频次，在windows上比不切片的写入性能降低100倍。在linux上比不切片性能降低10倍。多进程切片文件锁在windows使用pywin32，在linux上还是要fcntl实现。
    所以此类使用缓存1秒钟内的日志为一个长字符串再插入，大幅度地降低了文件加锁和解锁的次数，速度比不做多进程安全切片的文件写入速度更快。
    主动触发写入文件。
    """
    file_handler_list = []
    has_start_emit_all_file_handler = False  # 只能在windwos运行正常，windwos是多进程每个进程的变量has_start_emit_all_file_handler是独立的。linux是共享的。

    @classmethod
    def _emit_all_file_handler(cls):
        while True:
            for hr in cls.file_handler_list:
                # very_nb_print(hr.buffer_msgs_queue.qsize())
                hr.rollover_and_do_write()
            time.sleep(0.1)

    @classmethod
    def start_emit_all_file_handler(cls):
        pass
        Thread(target=cls._emit_all_file_handler, daemon=True).start()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer_msgs_queue = queue.SimpleQueue()
        atexit.register(self._when_exit)  # 如果程序属于立马就能结束的，需要在程序结束前执行这个钩子，防止不到最后一秒的日志没记录到。
        self.file_handler_list.append(self)
        if not self.has_start_emit_all_file_handler:
            self.__class__.has_start_emit_all_file_handler = True
            self.start_emit_all_file_handler()

    def _when_exit(self):
        pass
        self.rollover_and_do_write()

    def emit(self, record):
        """
        emit已经在logger的handle方法中加了锁，所以这里的重置上次写入时间和清除buffer_msgs不需要加锁了。
        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            self.buffer_msgs_queue.put(msg)
        except Exception:
            self.handleError(record)

    def rollover_and_do_write(self, ):
        # very_nb_print(self.buffer_msgs_queue.qsize())
        self._rollover_and_do_write()

    def _rollover_and_do_write(self):
        buffer_msgs = ''
        while True:
            try:
                msg = self.buffer_msgs_queue.get(block=False)
                buffer_msgs += msg + '\n'
                # if len(buffer_msgs) > 1000 * 1000 * 100:
                #     break
            except Empty:
                break
        if buffer_msgs:
            try:
                self._do_lock()
                try:
                    if self.shouldRollover(None):
                        self.doRollover()
                except Exception as e:
                    self._console_log("Unable to do rollover: %s" % (e,), stack=True)
                # very_nb_print(len(self._buffer_msgs))
                self.do_write(buffer_msgs)
            finally:
                self._do_unlock()





ConcurrentRotatingFileHandlerWithBufferInitiativeLinux = ConcurrentRotatingFileHandler


`````

--- **end of file: nb_log/handlers_concurrent_rotating_file_handler.py** (project: nb_log) --- 

---


--- **start of file: nb_log/handlers_loguru.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/handlers_loguru.py`

#### 📦 Imports

- `import logging`
- `import os`
- `import sys`
- `import typing`
- `import uuid`
- `from nb_log import nb_log_config_default`
- `from loguru._logger import Logger`
- `from loguru._logger import Core`

#### 🏛️ Classes (2)

##### 📌 `class LoguruStreamHandler(logging.Handler)`
*Line: 9*

**Docstring:**
`````
loguru 的 控制台效果
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, logger_name, sink: typing.Any = sys.stdout)`
  - **Parameters:**
    - `self`
    - `logger_name`
    - `sink: typing.Any = sys.stdout`

**Public Methods (1):**
- `def emit(self, record)`

**Class Variables (1):**
- `format = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[namespace]} | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'`

##### 📌 `class LoguruFileHandler(LoguruStreamHandler)`
*Line: 55*

**Docstring:**
`````
loguru 的 文件日志写入
`````


---

`````python
import logging
import os
import sys
import typing
import uuid
from nb_log import nb_log_config_default


class LoguruStreamHandler(logging.Handler):
    """
    loguru 的 控制台效果
    """

    format = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[namespace]} | "
              "<level>{level: <8}</level> | "
              "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    def __init__(self, logger_name, sink: typing.Any = sys.stdout):
        logging.Handler.__init__(self)
        self._logger_name = logger_name
        self._sink = sink
        from loguru._logger import Logger, Core

        logger = Logger(
            core=Core(),
            exception=None,
            depth=6,  # 写6是为了显示实际的日志发生处，而不是封装loguru的emit方法处。
            record=False,
            lazy=False,
            colors=False,
            raw=False,
            capture=True,
            patchers=[],
            extra={},
        )

        self._bind_for = uuid.uuid4()
        self._add_handler(logger, )
        # print(logger._core.handlers)
        self.logurux = logger.bind(namespace=logger_name,
                                   # bind_for = self._bind_for
                                   )


    def _add_handler(self, logger, ):
        logger.add(self._sink,
                   # filter=lambda record: record["extra"]["bind_for"] == self._bind_for,
                   format=self.format)


    def emit(self, record):
        self.logurux.opt(depth=6, exception=record.exc_info).log(record.levelname, record.getMessage())


class LoguruFileHandler(LoguruStreamHandler):
    """
    loguru 的 文件日志写入
    """

    def _add_handler(self, logger, ):
        '''

        :param logger:
        :return:
        '''
        log_file_full_path = self._sink
        # rotation = "100 MB"  "00:00"
        arr = log_file_full_path.split('.')
        part1 = '.'.join(arr[:-1])
        part2 = arr[-1]
        loguru_file = f'{part1}.{{time:YYYYMMDD}}.loguru.{part2}'

        # rotation_size = 1024 * 1024  # 1MB
        rotation_size = f"{nb_log_config_default.LOG_FILE_SIZE} MB"
        rotation_time = "00:00"  # 每天的 00:00

        logger.add(loguru_file,
                   # filter=lambda record: record["extra"]["bind_for"] == self._bind_for,
                   format=self.format,
                   enqueue=True,
                   # rotation=f"{nb_log_config_default.LOG_FILE_SIZE} MB",
                   rotation=rotation_time,
                   retention=nb_log_config_default.LOG_FILE_BACKUP_COUNT
                   )

`````

--- **end of file: nb_log/handlers_loguru.py** (project: nb_log) --- 

---


--- **start of file: nb_log/handlers_more.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/handlers_more.py`

#### 📦 Imports

- `import sys`
- `import os`
- `import threading`
- `import traceback`
- `import socket`
- `import datetime`
- `import json`
- `import time`
- `import typing`
- `from collections import OrderedDict`
- `from pathlib import Path`
- `from queue import Queue`
- `from queue import Empty`
- `from kafka import KafkaProducer`
- `from threading import Lock`
- `from threading import Thread`
- `import pymongo`
- `import logging`
- `from logging.handlers import WatchedFileHandler`
- `from nb_log.monkey_print import nb_print`
- `from elasticsearch import Elasticsearch`
- `from elasticsearch import helpers`
- `from elasticsearch import Elasticsearch`
- `from elasticsearch import helpers`

#### 🏛️ Classes (4)

##### 📌 `class MongoHandler(logging.Handler)`
*Line: 34*

**Docstring:**
`````
一个mongodb的log handler,支持日志按loggername创建不同的集合写入mongodb中
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, mongo_url, mongo_database = 'logs')`
  - **Docstring:**
  `````
  :param mongo_url:  mongo连接
  :param mongo_database: 保存日志的数据库，默认使用logs数据库
  `````
  - **Parameters:**
    - `self`
    - `mongo_url`
    - `mongo_database = 'logs'`

**Public Methods (1):**
- `def emit(self, record)`

##### 📌 `class KafkaHandler(logging.Handler)`
*Line: 92*

**Docstring:**
`````
日志批量写入kafka中。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, bootstrap_servers, **configs)`
  - **Docstring:**
  `````
  :param elastic_hosts:  es的ip地址，数组类型
  :param elastic_port：  es端口
  :param index_prefix: index名字前缀。
  `````
  - **Parameters:**
    - `self`
    - `bootstrap_servers`
    - `**configs`

**Public Methods (1):**
- `def emit(self, record)`

**Class Variables (10):**
- `ES_INTERVAL_SECONDS = 0.5`
- `host_name = host_name`
- `host_process = f'{host_name} -- {os.getpid()}'`
- `script_name = sys.argv[0].split('/')[-1]`
- `task_queue = Queue()`
- `last_es_op_time = time.time()`
- `has_start_do_bulk_op = False`
- `has_start_check_size_and_clear = False`
- `kafka_producer = None`
- `es_index_prefix = 'pylog-'`

##### 📌 `class ElasticHandler000(logging.Handler)`
*Line: 216*

**Docstring:**
`````
日志批量写入es中。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, elastic_hosts: list, elastic_port, index_prefix = 'pylog-')`
  - **Docstring:**
  `````
  :param elastic_hosts:  es的ip地址，数组类型
  :param elastic_port：  es端口
  :param index_prefix: index名字前缀。
  `````
  - **Parameters:**
    - `self`
    - `elastic_hosts: list`
    - `elastic_port`
    - `index_prefix = 'pylog-'`

**Public Methods (1):**
- `def emit(self, record)`

**Class Variables (2):**
- `ES_INTERVAL_SECONDS = 2`
- `host_name = host_name`

##### 📌 `class ElasticHandler(logging.Handler)`
*Line: 304*

**Docstring:**
`````
日志批量写入es中。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, elastic_hosts: list, elastic_port, index_prefix = 'pylog-')`
  - **Docstring:**
  `````
  :param elastic_hosts:  es的ip地址，数组类型
  :param elastic_port：  es端口
  :param index_prefix: index名字前缀。
  `````
  - **Parameters:**
    - `self`
    - `elastic_hosts: list`
    - `elastic_port`
    - `index_prefix = 'pylog-'`

**Public Methods (1):**
- `def emit(self, record)`

**Class Variables (7):**
- `ES_INTERVAL_SECONDS = 0.5`
- `host_name = host_name`
- `host_process = f'{host_name} -- {os.getpid()}'`
- `script_name = sys.argv[0]`
- `task_queue = Queue()`
- `last_es_op_time = time.time()`
- `has_start_do_bulk_op = False`


---

`````python
# noinspection PyMissingOrEmptyDocstring

import sys
import os
import threading
import traceback
import socket
import datetime
import json
import time
import typing

from collections import OrderedDict
from pathlib import Path
from queue import Queue, Empty
# noinspection PyPackageRequirements
from kafka import KafkaProducer
# from elasticsearch import Elasticsearch, helpers  # 性能导入时间消耗2秒,实例化时候再导入。
from threading import Lock, Thread
import pymongo

import logging

from logging.handlers import WatchedFileHandler

from nb_log.monkey_print import nb_print

very_nb_print = nb_print
os_name = os.name

host_name = socket.gethostname()


class MongoHandler(logging.Handler):
    """
    一个mongodb的log handler,支持日志按loggername创建不同的集合写入mongodb中
    """

    # msg_pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+) - (\S*?) - (\S*?) - (\d+) - (\S*?) - ([\s\S]*)')

    def __init__(self, mongo_url, mongo_database='logs'):
        """
        :param mongo_url:  mongo连接
        :param mongo_database: 保存日志的数据库，默认使用logs数据库
        """
        logging.Handler.__init__(self)
        mongo_client = pymongo.MongoClient(mongo_url)
        self.mongo_db = mongo_client.get_database(mongo_database)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            """以下使用解析日志模板的方式提取出字段"""
            # msg = self.format(record)
            # logging.LogRecord
            # msg_match = self.msg_pattern.search(msg)
            # log_info_dict = {'time': msg_match.group(1),
            #                  'name': msg_match.group(2),
            #                  'file_name': msg_match.group(3),
            #                  'line_no': msg_match.group(4),
            #                  'log_level': msg_match.group(5),
            #                  'detail_msg': msg_match.group(6),
            #                  }
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            log_info_dict['line_no'] = record.lineno
            log_info_dict['log_level'] = level_str
            log_info_dict['detail_msg'] = record.msg
            col = self.mongo_db.get_collection(record.name)
            col.insert_one(log_info_dict)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class KafkaHandler(logging.Handler):
    """
    日志批量写入kafka中。
    """
    ES_INTERVAL_SECONDS = 0.5

    host_name = host_name
    host_process = f'{host_name} -- {os.getpid()}'

    script_name = sys.argv[0].split('/')[-1]

    task_queue = Queue()
    last_es_op_time = time.time()
    has_start_do_bulk_op = False
    has_start_check_size_and_clear = False

    kafka_producer = None
    es_index_prefix = 'pylog-'

    def __init__(self, bootstrap_servers, **configs):
        """
        :param elastic_hosts:  es的ip地址，数组类型
        :param elastic_port：  es端口
        :param index_prefix: index名字前缀。
        """
        logging.Handler.__init__(self)
        if not self.__class__.kafka_producer:
            very_nb_print('实例化kafka producer')
            self.__class__.kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, **configs)

        t = Thread(target=self._do_bulk_op)
        t.setDaemon(True)
        t.start()

    @classmethod
    def __add_task_to_bulk(cls, task):
        cls.task_queue.put(task)

    # noinspection PyUnresolvedReferences
    @classmethod
    def __clear_bulk_task(cls):
        cls.task_queue.queue.clear()

    @classmethod
    def _check_size_and_clear(cls):
        """
        如果是外网传输日志到测试环境风险很大，测试环境网络经常打满，传输不了会造成日志队列堆积，会造成内存泄漏，所以需要清理。
        :return:
        """
        if cls.has_start_check_size_and_clear:
            return
        cls.has_start_check_size_and_clear = True

        def __check_size_and_clear():
            while 1:
                size = cls.task_queue.qsize()
                if size > 1000:
                    very_nb_print(f'kafka防止意外日志积累太多了,达到 {size} 个，为防止内存泄漏，清除队列')
                    cls.__clear_bulk_task()
                time.sleep(0.1)

        t = Thread(target=__check_size_and_clear)
        t.setDaemon(True)
        t.start()

    @classmethod
    def _do_bulk_op(cls):
        if cls.has_start_do_bulk_op:
            return

        cls.has_start_do_bulk_op = True
        # very_nb_print(cls.kafka_producer)
        while 1:
            try:
                # noinspection PyUnresolvedReferences
                tasks = list(cls.task_queue.queue)
                cls.__clear_bulk_task()
                for task in tasks:
                    topic = (cls.es_index_prefix + task['name']).replace('.', '').replace('_', '').replace('-', '')
                    # very_nb_print(topic)
                    cls.kafka_producer.send(topic, json.dumps(task).encode())
                cls.last_es_op_time = time.time()
            except Exception as e:
                very_nb_print(e)
            finally:
                time.sleep(cls.ES_INTERVAL_SECONDS)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['@timestamp'] = datetime.datetime.utcfromtimestamp(record.created).isoformat()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['host'] = self.host_name
            log_info_dict['host_process'] = self.host_process
            # log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            # log_info_dict['line_no'] = record.lineno
            log_info_dict['log_place'] = f'{record.pathname}:{record.lineno}'
            log_info_dict['log_level'] = level_str
            log_info_dict['msg'] = str(record.msg)
            log_info_dict['script'] = self.script_name
            log_info_dict['es_index'] = f'{self.es_index_prefix}{record.name.lower()}'
            self.__add_task_to_bulk(log_info_dict)

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class ElasticHandler000(logging.Handler):
    """
    日志批量写入es中。
    """
    ES_INTERVAL_SECONDS = 2
    host_name = host_name

    def __init__(self, elastic_hosts: list, elastic_port, index_prefix='pylog-'):
        """
        :param elastic_hosts:  es的ip地址，数组类型
        :param elastic_port：  es端口
        :param index_prefix: index名字前缀。
        """
        from elasticsearch import Elasticsearch, helpers
        self._helpers = helpers
        logging.Handler.__init__(self)
        self._es_client = Elasticsearch(elastic_hosts, port=elastic_port)
        self._index_prefix = index_prefix
        self._task_list = []
        self._task_queue = Queue()
        self._last_es_op_time = time.time()
        t = Thread(target=self._do_bulk_op)
        t.setDaemon(True)
        t.start()

    def __add_task_to_bulk(self, task):
        self._task_queue.put(task)

    def __clear_bulk_task(self):
        # noinspection PyUnresolvedReferences
        self._task_queue.queue.clear()

    def _do_bulk_op(self):
        while 1:
            try:
                if self._task_queue.qsize() > 10000:
                    very_nb_print('防止意外日志积累太多了，不插入es了。')
                    self.__clear_bulk_task()
                    return
                # noinspection PyUnresolvedReferences
                tasks = list(self._task_queue.queue)
                self.__clear_bulk_task()
                self._helpers.bulk(self._es_client, tasks)

                self._last_es_op_time = time.time()
            except Exception as e:
                very_nb_print(e)
            finally:
                time.sleep(1)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['@timestamp'] = datetime.datetime.utcfromtimestamp(record.created).isoformat()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['host'] = self.host_name
            log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            log_info_dict['line_no'] = record.lineno
            log_info_dict['log_level'] = level_str
            log_info_dict['msg'] = str(record.msg)
            self.__add_task_to_bulk({
                "_index": f'{self._index_prefix}{record.name.lower()}',
                # "_type": '_doc',  # elastic 7 服务端之后不要传递 type了.
                "_source": log_info_dict
            })

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


# noinspection PyUnresolvedReferences
class ElasticHandler(logging.Handler):
    """
    日志批量写入es中。
    """
    ES_INTERVAL_SECONDS = 0.5

    host_name = host_name
    host_process = f'{host_name} -- {os.getpid()}'

    script_name = sys.argv[0]

    task_queue = Queue()
    last_es_op_time = time.time()
    has_start_do_bulk_op = False

    def __init__(self, elastic_hosts: list, elastic_port, index_prefix='pylog-'):
        """
        :param elastic_hosts:  es的ip地址，数组类型
        :param elastic_port：  es端口
        :param index_prefix: index名字前缀。
        """
        logging.Handler.__init__(self)
        from elasticsearch import Elasticsearch, helpers
        self._helpers = helpers
        self._es_client = Elasticsearch(elastic_hosts, )
        self._index_prefix = index_prefix
        t = Thread(target=self._do_bulk_op)
        t.setDaemon(True)
        t.start()

    @classmethod
    def __add_task_to_bulk(cls, task):
        cls.task_queue.put(task)

    # noinspection PyUnresolvedReferences
    @classmethod
    def __clear_bulk_task(cls):
        cls.task_queue.queue.clear()

    def _do_bulk_op(self):
        if self.__class__.has_start_do_bulk_op:
            return
        self.__class__.has_start_do_bulk_op = True
        while 1:
            try:
                if self.__class__.task_queue.qsize() > 10000:
                    very_nb_print('防止意外日志积累太多了，不插入es了。')
                    self.__clear_bulk_task()
                    return
                tasks = list(self.__class__.task_queue.queue)
                self.__clear_bulk_task()
                self._helpers.bulk(self._es_client, tasks)
                self.__class__.last_es_op_time = time.time()
            except Exception as e:
                very_nb_print(e)
            finally:
                time.sleep(self.ES_INTERVAL_SECONDS)

    def emit(self, record):
        # noinspection PyBroadException, PyPep8
        try:
            level_str = None
            if record.levelno == 10:
                level_str = 'DEBUG'
            elif record.levelno == 20:
                level_str = 'INFO'
            elif record.levelno == 30:
                level_str = 'WARNING'
            elif record.levelno == 40:
                level_str = 'ERROR'
            elif record.levelno == 50:
                level_str = 'CRITICAL'
            log_info_dict = OrderedDict()
            log_info_dict['@timestamp'] = datetime.datetime.utcfromtimestamp(record.created).isoformat()
            log_info_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            log_info_dict['name'] = record.name
            log_info_dict['host'] = self.host_name
            log_info_dict['host_process'] = self.host_process
            log_info_dict['file_path'] = record.pathname
            log_info_dict['file_name'] = record.filename
            log_info_dict['func_name'] = record.funcName
            log_info_dict['line_no'] = record.lineno
            log_info_dict['log_level'] = level_str
            log_info_dict['msg'] = str(record.msg)
            log_info_dict['script'] = self.script_name
            self.__add_task_to_bulk({
                "_index": f'{self._index_prefix}{record.name.lower()}',
                # "_type": f'_doc',    # es7 服务端之后不支持_type设置
                "_source": log_info_dict
            })

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

`````

--- **end of file: nb_log/handlers_more.py** (project: nb_log) --- 

---


--- **start of file: nb_log/helpers.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/helpers.py`

#### 📦 Imports

- `import logging`

#### 🔧 Public Functions (1)

- `def generate_error_file_name(log_filename: str)`
  - *Line: 4*
  - **Docstring:**
  `````
  根据正常日志文件名,自动生成错误日志文件名.
  :param log_filename:
  :return:
  `````


---

`````python
import logging


def generate_error_file_name(log_filename: str):
    """
    根据正常日志文件名,自动生成错误日志文件名.
    :param log_filename:
    :return:
    """
    if log_filename is None:
        return None
    arr = log_filename.split('.')
    part1 = '.'.join(arr[:-1])
    part2 = arr[-1]
    return f'{part1}.error.{part2}'




`````

--- **end of file: nb_log/helpers.py** (project: nb_log) --- 

---


--- **start of file: nb_log/logging_tree_helper.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/logging_tree_helper.py`

#### 📦 Imports

- `from logging_tree import printout`
- `import funboost`


---

`````python

from logging_tree import printout

if __name__ == '__main__':
    import funboost
    printout()
`````

--- **end of file: nb_log/logging_tree_helper.py** (project: nb_log) --- 

---


--- **start of file: nb_log/log_manager.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/log_manager.py`

#### 📝 Module Docstring

`````
日志管理，支持日志打印到控制台和写入切片文件和mongodb和email和钉钉机器人和elastic和kafka。
建造者模式一键创建返回添加了各种好用的handler的原生官方Logger对象，兼容性扩展性极强。
使用观察者模式按照里面的例子可以扩展各种有趣的handler。
使用方式为  logger = LogManager('logger_name').get_and_add_handlers(log_level_int=1, is_add_stream_handler=True,
 log_path=None, _log_filename=None, log_file_size=10,mongo_url=None,formatter_template=2)


concurrent_log_handler的ConcurrentRotatingFileHandler解决了logging模块自带的RotatingFileHandler多进程切片错误，
此ConcurrentRotatingFileHandler在win和linux多进程场景下log文件切片都ok.

1、根据日志级别，使用coolorhanlder代替straemhandler打印5种颜色的日志，一目了然哪里是严重的日志。
2、带有多种handler，邮件 mongo stream file的。
3、支持pycharm点击日志跳转到对应代码文件的对应行。
4、对相同命名空间的logger可以无限添加同种类型的handlers，不会重复使用同种handler记录日志。不需要用户自己去判断。
5、更新文件日志性能，基于ConcurrentRotatingFileHandler继承重写，使用缓存1秒内的消息成批量的方式插入，
使极限多进程安全切片的文件日志写入性能在win下提高100倍，linux下提高10倍。
`````

#### 📦 Imports

- `import logging`
- `import multiprocessing`
- `import threading`
- `import typing`
- `from functools import lru_cache`
- `from logging import FileHandler`
- `from logging import _checkLevel`
- `from nb_log import nb_log_config_default`
- `from nb_log.loggers_imp.compatible_logger import CompatibleLogger`
- `from nb_log.handlers import *`
- `import deprecated`
- `from nb_log.helpers import generate_error_file_name`
- `from nb_log.handlers_more import MongoHandler`
- `from nb_log.handlers_more import ElasticHandler`
- `from nb_log.handlers_more import KafkaHandler`
- `from nb_log.handlers_loguru import LoguruStreamHandler`
- `from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos`
- `from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandlerWithBufferInitiativeLinux`
- `from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandler`
- `from nb_log.handlers_loguru import LoguruFileHandler`

#### 🏛️ Classes (10)

##### 📌 `class _Undefind`
*Line: 155*

##### 📌 `class DataClassBase`
*Line: 163*

**Docstring:**
`````
使用类实现的
相比与字典，数据类在ide下补全犀利。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, **kwargs)`
  - **Parameters:**
    - `self`
    - `**kwargs`

**Public Methods (2):**
- `def get_dict(self)`
- `def get_json(self)`

##### 📌 `class MailHandlerConfig(DataClassBase)`
*Line: 197*

**Class Variables (9):**
- `mailhost: tuple = nb_log_config_default.EMAIL_HOST`
- `fromaddr: str = nb_log_config_default.EMAIL_FROMADDR`
- `toaddrs: tuple = nb_log_config_default.EMAIL_TOADDRS`
- `subject: str = 'xx项目邮件日志报警'`
- `credentials: tuple = nb_log_config_default.EMAIL_CREDENTIALS`
- `secure = None`
- `timeout = 5.0`
- `is_use_ssl = True`
- `mail_time_interval = 60`

##### 📌 `class LogManager(object)`
*Line: 230*

**Docstring:**
`````
一个日志管理类，用于创建logger和添加handler，支持将日志打印到控制台打印和写入日志文件和mongodb和邮件。
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, logger_name: typing.Union[str, None] = 'nb_log_default_namespace', logger_cls = logging.Logger)`
  - **Docstring:**
  `````
  :param logger_name: 日志名称，当为None时候创建root命名空间的日志，一般情况下千万不要传None，除非你确定需要这么做和是在做什么.这个命名空间是双刃剑
  `````
  - **Parameters:**
    - `self`
    - `logger_name: typing.Union[str, None] = 'nb_log_default_namespace'`
    - `logger_cls = logging.Logger`

**Public Methods (8):**
- `def get_all_logging_name()` `staticmethod`
- `def preset_log_level(self, log_level_int = 20)`
  - **Docstring:**
  `````
  提前设置锁定日志级别，当之后再设置该命名空间日志的级别的时候，按照提前预设的级别，无视之后设定的级别。
  主要是针对动态初始化的日志，在生成日志之后再去设置日志级别不方便。
  :param log_level_int:logging.DEBUG LOGGING.INFO 等
  :return:
  `````
- `def prevent_add_handlers(self)`
  - *对命名空间设置阻止添加handlers*
- `def get_logger_and_add_handlers(self, log_level_int: int = None) -> logging.Logger`
  - **Docstring:**
  `````
  :param log_level_int: 日志输出级别，设置为 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，
  :param is_add_stream_handler: 是否打印日志到控制台
  :param is_use_loguru_stream_handler  是否使用 loguru的控制台打印，如果为None，使用 nb_log_config.py的DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER 值。
  :param do_not_use_color_handler :是否禁止使用color彩色日志
  :param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
         非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
  :param log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
  :param error_log_filename :错误日志文件名字，如果文件名不为None，那么error级别以上日志自动写入到这个错误文件。
  :param log_file_size :日志大小，单位M，默认100M
  :param log_file_handler_type :这个值可以设置为1 2 3 4 5 6 7，1为使用多进程安全按日志文件大小切割的文件日志
         2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
         3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
         4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
         5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
           这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
         6 为作者发明的高性能多进程安全，同时按大小和时间切割的文件日志handler
         7 为 loguru的 文件日志记录器
  :param mongo_url : mongodb的连接，为None时候不添加mongohandler
  :param is_add_elastic_handler: 是否记录到es中。
  :param is_add_kafka_handler: 日志是否发布到kafka。
  :param ding_talk_token:钉钉机器人token
  :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
  :param mail_handler_config : 邮件配置
  :param is_add_mail_handler :是否发邮件
  :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                           1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                           如果为logging.Formatter对象，则直接使用用户传入的模板。
  :type log_level_int :int
  :type is_add_stream_handler :bool
  :type log_path :str
  :type log_filename :str
  :type mongo_url :str
  :type log_file_size :int
  `````
- `def get_logger_without_handlers(self)`
  - *返回一个不带hanlers的logger*
- `def look_over_all_handlers(self)`
- `def remove_all_handlers(self)`
- `def remove_handler_by_handler_class(self, handler_class: typing.Union[type, str])`
  - **Docstring:**
  `````
  去掉指定类型的handler
  :param handler_class:logging.StreamHandler,ColorHandler,MongoHandler,ConcurrentRotatingFileHandler,MongoHandler,CompatibleSMTPSSLHandler的一种
  :return:
  `````

**Class Variables (4):**
- `logger_name_list = []`
- `logger_list = []`
- `preset_name__level_map = dict()`
- `logger_name__logger_cls_obj_map = {}`

##### 📌 `class LoggerLevelSetterMixin`
*Line: 614*

**Public Methods (1):**
- `def set_log_level(self, log_level = 10)`

##### 📌 `class LoggerMixin(LoggerLevelSetterMixin)`
*Line: 625*

**Docstring:**
`````
主要是生成把类名作为日志命名空间的logger，方便被混入类直接使用self.logger，不需要手动实例化get_logger。
`````

**Properties (3):**
- `@property logger_full_name`
- `@property logger -> logging.Logger`
- `@property logger_with_file -> logging.Logger`

**Class Variables (2):**
- `subclass_logger_dict = {}`
- `logger_extra_suffix = ''`

##### 📌 `class LoggerMixinDefaultWithFileHandler(LoggerMixin)`
*Line: 661*

**Properties (1):**
- `@property logger`

**Class Variables (1):**
- `subclass_logger_dict = {}`

##### 📌 `class MetaTypeLogger(type)`
*Line: 679*

**🔧 Constructor (`__init__`):**
- `def __init__(cls, name, bases, attrs)`
  - **Parameters:**
    - `cls`
    - `name`
    - `bases`
    - `attrs`

##### 📌 `class MetaTypeFileLogger(type)`
*Line: 685*

**🔧 Constructor (`__init__`):**
- `def __init__(cls, name, bases, attrs)`
  - **Parameters:**
    - `cls`
    - `name`
    - `bases`
    - `attrs`

##### 📌 `class LoggedException(Exception)`
*Line: 714*

**Docstring:**
`````
抛出异常的同时,自动记录日志到日志文件中,这样就不需要每次都raise,并写日志日路,分两行来写了.
try :
    1/0
except Exception as e:
    raise LoggedException(message='有问题',)
`````

**🔧 Constructor (`__init__`):**
- `def __init__(self, message: str, logger_obj = None, exc_info = True)`
  - **Docstring:**
  `````
  :param message:
  :param logger_obj: 传递logger对象,使用指定的logger来记录日志,那就log_filename不起作用
  :param exc_info: 日志是否记录仪详细报错堆栈
  `````
  - **Parameters:**
    - `self`
    - `message: str`
    - `logger_obj = None`
    - `exc_info = True`

#### 🔧 Public Functions (11)

- `def revision_call_handlers(self, record)`
  - *Line: 46*
  - **Docstring:**
  `````
  重要。这可以使同名logger或父logger随意添加同种类型的handler，确保不会重复打印。
  例如对"a"命名空间加上streamhandler，对"a.b"命名空间也加上streamhandler，则"a.b"命名空间的日志会被打印两次
  例子如下
  
  import logging
  
  logger1 = logging.getLogger('a')
  logger1.addHandler(logging.StreamHandler())
  
  logger2 = logging.getLogger('a.b')
  logger2.addHandler(logging.StreamHandler())
  
  logger2.error(666)
  
  明明只想打印一次666，结果却答应2次了。因为a.b的父命名空间的日志也加了streamhandler。
  
  :param self:
  :param record:
  :return:
  `````

- `def revision_add_handler(self, hdlr)`
  - *Line: 109*
  - *Add the specified handler to this logger.*

- `def revision_setLevel(self, level)`
  - *Line: 134*
  - *Set the logging level of this logger.  level must be an int or a str.*

- `def get_all_logging_name()`
  - *Line: 209*

- `def get_all_handlers()`
  - *Line: 214*

- `def check_log_level(log_level: int)`
  - *Line: 224*

- `def get_logger(name: typing.Union[str, None]) -> logging.Logger` `lru_cache()`
  - *Line: 545*
  - **Docstring:**
  `````
  重写一遍，是为了更好的pycharm自动补全，所以不用**kwargs的写法。
  如果太喜欢函数调用了，可以使用这种.
  get_logger_and_add_handlers是LogManager类最常用的公有方法，其他方法使用场景的频率比较低，
  但如果要使用那些低频率功能，还是要亲自调用LogManger类，而不是仅仅只了解此函数的用法。
      :param name 日志命名空间，这个是最重要最难理解的一个入参，很多pythoner到现在还不知道name是什么作用。日志命名空间，意义非常非常非常重要，有些人到现在还不知道 logging.getLogger() 第一个入参的作用，太low了。不同的name的logger可以表现出不同的行为。
              例如让 aa命名空间的日志打印控制台并且写入到文件，并且只记录info级别以上，让 bb 命名空间的日志仅仅打印控制台，并且打印debug以上级别，
              这种就可以通过不同的日志命名空间做到。
      :param log_level_int: 日志输出级别，设置为 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，现在可以直接用10 20 30 40 50了，兼容了。
     :param is_add_stream_handler: 是否打印日志到控制台
     :param is_use_loguru_stream_handler  是否使用 loguru的控制台打印，如果为None，使用 nb_log_config.py的DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER 值。
     :param do_not_use_color_handler :是否禁止使用color彩色日志
     :param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
            非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
     :param log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
     :param error_log_filename :错误日志文件名字，如果文件名不为None，那么error级别以上日志自动写入到这个错误文件。
     :param log_file_size :日志大小，单位M，默认100M
     :param log_file_handler_type :这个值可以设置为1 2 3 4 5 6 7，1为使用多进程安全按日志文件大小切割的文件日志
            2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
            3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
            4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
            5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
              这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
            6 为作者发明的高性能多进程安全，同时按大小和时间切割的文件日志handler
            7 为 loguru的 文件日志记录器
     :param mongo_url : mongodb的连接，为None时候不添加mongohandler
     :param is_add_elastic_handler: 是否记录到es中。
     :param is_add_kafka_handler: 日志是否发布到kafka。
     :param ding_talk_token:钉钉机器人token
     :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
     :param mail_handler_config : 邮件配置
     :param is_add_mail_handler :是否发邮件
     :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                              1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                              如果为logging.Formatter对象，则直接使用用户传入的模板。
     :type log_level_int :int
     :type is_add_stream_handler :bool
     :type log_path :str
     :type log_filename :str
     :type mongo_url :str
     :type log_file_size :int
  `````

- `def get_logger_with_filehanlder(name: str) -> logging.Logger` `lru_cache()`
  - *Line: 605*
  - **Docstring:**
  `````
  默认添加color handler  和 文件日志。
  :param name:
  :return:
  `````

- `def logger_catch(logger: logging.Logger, reraise: bool = True, show_trace_back = True)`
  - *Line: 691*

- `def build_exception_logger()` `lru_cache()`
  - *Line: 709*

- `def logged_raise(e: BaseException, logger_obj = None, exc_info = True)`
  - *Line: 740*
  - **Docstring:**
  `````
  try :
      1/0
  except Exception as e:
      logged_raise(ZeroDivisionError('0不能是被除数'))
  
  :param e:
  :param logger_obj:
  :param exc_info:
  :return:
  `````


---

`````python
# coding=utf8
# noinspection SpellCheckingInspection
"""
日志管理，支持日志打印到控制台和写入切片文件和mongodb和email和钉钉机器人和elastic和kafka。
建造者模式一键创建返回添加了各种好用的handler的原生官方Logger对象，兼容性扩展性极强。
使用观察者模式按照里面的例子可以扩展各种有趣的handler。
使用方式为  logger = LogManager('logger_name').get_and_add_handlers(log_level_int=1, is_add_stream_handler=True,
 log_path=None, _log_filename=None, log_file_size=10,mongo_url=None,formatter_template=2)


concurrent_log_handler的ConcurrentRotatingFileHandler解决了logging模块自带的RotatingFileHandler多进程切片错误，
此ConcurrentRotatingFileHandler在win和linux多进程场景下log文件切片都ok.

1、根据日志级别，使用coolorhanlder代替straemhandler打印5种颜色的日志，一目了然哪里是严重的日志。
2、带有多种handler，邮件 mongo stream file的。
3、支持pycharm点击日志跳转到对应代码文件的对应行。
4、对相同命名空间的logger可以无限添加同种类型的handlers，不会重复使用同种handler记录日志。不需要用户自己去判断。
5、更新文件日志性能，基于ConcurrentRotatingFileHandler继承重写，使用缓存1秒内的消息成批量的方式插入，
使极限多进程安全切片的文件日志写入性能在win下提高100倍，linux下提高10倍。

"""
import logging
import multiprocessing
import threading
import typing
from functools import lru_cache
from logging import FileHandler, _checkLevel  # noqa
from nb_log import nb_log_config_default  # noqa
from nb_log.loggers_imp.compatible_logger import CompatibleLogger
from nb_log.handlers import *
import deprecated

from nb_log.helpers import generate_error_file_name

MANUAL_HANLDER_TYPE = 'manual_hanlder_type'
HANDLER_TYPE_FILE = 'HANDLER_TYPE_FILE'
HANDLER_TYPE_ERROR_FILE = 'HANDLER_TYPE_ERROR_FILE'
HANDLER_TYPE_STREAM = 'HANDLER_TYPE_STREAM'


def _get_hanlder_type(handlerx: logging.Handler):
    return getattr(handlerx, MANUAL_HANLDER_TYPE, None) or type(handlerx)


# noinspection DuplicatedCode
def revision_call_handlers(self, record):  # 对logging标准模块打猴子补丁。主要是使父命名空间的handler不重复记录当前命名空间日志已有种类的handler。
    """
    重要。这可以使同名logger或父logger随意添加同种类型的handler，确保不会重复打印。
    例如对"a"命名空间加上streamhandler，对"a.b"命名空间也加上streamhandler，则"a.b"命名空间的日志会被打印两次
    例子如下

    import logging

    logger1 = logging.getLogger('a')
    logger1.addHandler(logging.StreamHandler())

    logger2 = logging.getLogger('a.b')
    logger2.addHandler(logging.StreamHandler())

    logger2.error(666)

    明明只想打印一次666，结果却答应2次了。因为a.b的父命名空间的日志也加了streamhandler。

    :param self:
    :param record:
    :return:
    """

    """
    Pass a record to all relevant handlers.

    Loop through all handlers for this logger and its parents in the
    logger hierarchy. If no handler was found, output a one-off error
    message to sys.stderr. Stop searching up the hierarchy whenever a
    logger with the "propagate" attribute set to zero is found - that
    will be the last logger whose handlers are called.
    """
    c = self
    found = 0
    hdlr_type_set = set()

    while c:
        for hdlr in c.handlers:
            hdlr_type = _get_hanlder_type(hdlr)
            # if hdlr_type == logging.StreamHandler:  # REMIND 因为很多handler都是继承自StreamHandler，包括filehandler，直接判断会逻辑出错。
            #     hdlr_type = ColorHandler
            found = found + 1
            if record.levelno >= hdlr.level:
                if hdlr_type not in hdlr_type_set:
                    hdlr.handle(record)
                hdlr_type_set.add(hdlr_type)
        if not c.propagate:
            c = None  # break out
        else:
            c = c.parent
    # noinspection PyRedundantParentheses
    if (found == 0):
        if logging.lastResort:
            if record.levelno >= logging.lastResort.level:
                logging.lastResort.handle(record)
        elif logging.raiseExceptions and not self.manager.emittedNoHandlerWarning:
            sys.stderr.write("No handlers could be found for logger"
                             " \"%s\"\n" % self.name)
            sys.stderr.flush()
            self.manager.emittedNoHandlerWarning = True

_lock = threading.Lock()
# noinspection PyProtectedMember
def revision_add_handler(self, hdlr):  # 从添加源头阻止同一个logger添加同类型的handler。
    """
    Add the specified handler to this logger.
    """
    # logging._acquireLock()  # noqa
    """ 官方的
    if not (hdlr in self.handlers):
        self.handlers.append(hdlr)
    """
    with _lock:
        hdlrx_type_set = set()
        for hdlrx in self.handlers:
            hdlrx_type = _get_hanlder_type(hdlrx)
            # if hdlrx_type == logging.StreamHandler:  # REMIND 因为很多handler都是继承自StreamHandler，包括filehandler，直接判断会逻辑出错。
            #     hdlrx_type = ColorHandler
            hdlrx_type_set.add(hdlrx_type)

        hdlr_type = _get_hanlder_type(hdlr)
        # if hdlr_type == logging.StreamHandler:
        #     hdlr_type = ColorHandler
        if hdlr_type not in hdlrx_type_set:
            self.handlers.append(hdlr)



def revision_setLevel(self, level):
    """
    Set the logging level of this logger.  level must be an int or a str.
    """
    level2 = LogManager.preset_name__level_map.get(self.name, level)
    if level2 != level:
        very_nb_print(f'日志命名空间 {self.name} 锁定了为了 {level2} 级别 ,后续不可以更改为 {level} 级别')
    self.level = _checkLevel(level2)
    if sys.version_info.minor >= 7:  # python3.6 没有 _clear_cache 方法
        self.manager._clear_cache()


logging.Logger.callHandlers = revision_call_handlers  # 打猴子补丁。
logging.Logger.addHandler = revision_add_handler  # 打猴子补丁。
logging.Logger.setLevel = revision_setLevel  # 打猴子补丁。


# noinspection PyShadowingBuiltins
# print = very_nb_print


class _Undefind:
    pass


undefind = _Undefind()


# noinspection DuplicatedCode
class DataClassBase:
    """
    使用类实现的
    相比与字典，数据类在ide下补全犀利。
    """

    def __new__(cls, **kwargs):
        self = super().__new__(cls)
        self.__dict__ = copy.deepcopy({k: v for k, v in cls.__dict__.items() if not k.startswith('__')})
        return self

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, ) -> dict:
        return self.get_dict()

    def get_dict(self):
        return {k: v.get_dict() if isinstance(v, DataClassBase) else v for k, v in self.__dict__.items()}

    def get_json(self):
        return json.dumps(self.get_dict(), ensure_ascii=False, indent=4)

    def __str__(self):
        return f"{self.__class__}    {self.get_json()}"

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class MailHandlerConfig(DataClassBase):
    mailhost: tuple = nb_log_config_default.EMAIL_HOST
    fromaddr: str = nb_log_config_default.EMAIL_FROMADDR
    toaddrs: tuple = nb_log_config_default.EMAIL_TOADDRS
    subject: str = 'xx项目邮件日志报警'
    credentials: tuple = nb_log_config_default.EMAIL_CREDENTIALS
    secure = None
    timeout = 5.0
    is_use_ssl = True
    mail_time_interval = 60


def get_all_logging_name():
    logger_names = logging.Logger.manager.loggerDict.keys()
    return logger_names


def get_all_handlers():
    logger_names = get_all_logging_name()
    for name in list(logger_names) + ['root', None]:
        logx = logging.getLogger(name)
        print(name, logx.level, logx.handlers)


LOG_LEVEL_LIST = [logging.NOTSET,logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]  # 就是 10 20 30 40 50


def check_log_level(log_level: int):
    if log_level not in LOG_LEVEL_LIST:
        raise ValueError(f'你设置的日志级别不正确,你设置的级别是 {log_level} ，日志级别必须是 {LOG_LEVEL_LIST} 其中之一')


# noinspection PyMissingOrEmptyDocstring,PyPep8
class LogManager(object):
    """
    一个日志管理类，用于创建logger和添加handler，支持将日志打印到控制台打印和写入日志文件和mongodb和邮件。
    """
    logger_name_list = []
    logger_list = []
    preset_name__level_map = dict()
    logger_name__logger_cls_obj_map = {}

    @staticmethod
    def get_all_logging_name():
        return get_all_logging_name()

    def __init__(self, logger_name: typing.Union[str, None] = 'nb_log_default_namespace', logger_cls=logging.Logger):
        """
        :param logger_name: 日志名称，当为None时候创建root命名空间的日志，一般情况下千万不要传None，除非你确定需要这么做和是在做什么.这个命名空间是双刃剑
        """
        if logger_name in (None, '',) and multiprocessing.process.current_process().name == 'MainProcess':
            pass
            # very_nb_print('logger_name 设置为None和空字符串都是一个意义，在操作根日志命名空间，任何其他日志的行为将会发生变化，'
            #               '一定要弄清楚原生logging包的日志name的意思。这个命名空间是双刃剑')
        self._logger_name = logger_name
        self.logger: logging.Logger
        if logger_cls == logging.Logger:
            self.logger = logging.getLogger(logger_name)
        else:
            if logger_name not in self.logger_name__logger_cls_obj_map:
                self.logger = logger_cls(logger_name)
                self.logger_name__logger_cls_obj_map[logger_name] = self.logger
            else:
                self.logger = self.logger_name__logger_cls_obj_map[logger_name]

    def preset_log_level(self, log_level_int=20):
        """
        提前设置锁定日志级别，当之后再设置该命名空间日志的级别的时候，按照提前预设的级别，无视之后设定的级别。
        主要是针对动态初始化的日志，在生成日志之后再去设置日志级别不方便。
        :param log_level_int:logging.DEBUG LOGGING.INFO 等
        :return:
        """
        check_log_level(log_level_int)
        self.preset_name__level_map[self._logger_name or 'root'] = log_level_int
        self.logger.setLevel(log_level_int)

    def prevent_add_handlers(self):
        """对命名空间设置阻止添加handlers"""

        def _add_handler(handler: logging.Handler):
            pass

        self.logger.addHandler = _add_handler

    # 加*是为了强制在调用此方法时候使用关键字传参，如果以位置传参强制报错，因为此方法后面的参数中间可能以后随时会增加更多参数，造成之前的使用位置传参的代码参数意义不匹配。
    # noinspection PyAttributeOutsideInit
    def get_logger_and_add_handlers(self, log_level_int: int = None, *, is_add_stream_handler=True,
                                    is_use_loguru_stream_handler: bool = None,
                                    do_not_use_color_handler=None, log_path=None,
                                    log_filename=None, log_file_size: int = None,
                                    log_file_handler_type: int = None,
                                    error_log_filename=None,
                                    mongo_url=None, is_add_elastic_handler=False, is_add_kafka_handler=False,
                                    ding_talk_token=None, ding_talk_time_interval=60,
                                    mail_handler_config: MailHandlerConfig = MailHandlerConfig(),
                                    is_add_mail_handler=False,
                                    formatter_template: typing.Union[int, logging.Formatter] = None) -> logging.Logger:
        """
       :param log_level_int: 日志输出级别，设置为 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，
       :param is_add_stream_handler: 是否打印日志到控制台
       :param is_use_loguru_stream_handler  是否使用 loguru的控制台打印，如果为None，使用 nb_log_config.py的DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER 值。
       :param do_not_use_color_handler :是否禁止使用color彩色日志
       :param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
              非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
       :param log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
       :param error_log_filename :错误日志文件名字，如果文件名不为None，那么error级别以上日志自动写入到这个错误文件。
       :param log_file_size :日志大小，单位M，默认100M
       :param log_file_handler_type :这个值可以设置为1 2 3 4 5 6 7，1为使用多进程安全按日志文件大小切割的文件日志
              2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
              3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
              4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
              5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
                这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
              6 为作者发明的高性能多进程安全，同时按大小和时间切割的文件日志handler
              7 为 loguru的 文件日志记录器
       :param mongo_url : mongodb的连接，为None时候不添加mongohandler
       :param is_add_elastic_handler: 是否记录到es中。
       :param is_add_kafka_handler: 日志是否发布到kafka。
       :param ding_talk_token:钉钉机器人token
       :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
       :param mail_handler_config : 邮件配置
       :param is_add_mail_handler :是否发邮件
       :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                                1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                                如果为logging.Formatter对象，则直接使用用户传入的模板。
       :type log_level_int :int
       :type is_add_stream_handler :bool
       :type log_path :str
       :type log_filename :str
       :type mongo_url :str
       :type log_file_size :int
       """
        if log_level_int is None:
            log_level_int = nb_log_config_default.LOG_LEVEL_FILTER
        if do_not_use_color_handler is None:
            do_not_use_color_handler = not nb_log_config_default.DEFAULUT_USE_COLOR_HANDLER
        if log_filename is None and nb_log_config_default.DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER:
            log_filename = f'{self._logger_name}.log'
        if log_file_size is None:
            log_file_size = nb_log_config_default.LOG_FILE_SIZE
        if log_path is None:
            # print(nb_log_config_default.LOG_PATH)
            log_path = nb_log_config_default.LOG_PATH or '/pythonlogs'
        if formatter_template is None:
            formatter_template = nb_log_config_default.FORMATTER_KIND

        check_log_level(log_level_int)
        self._logger_level = log_level_int
        # if self._logger_name in self.preset_name__level_map:
        #     # print(self.preset_name__level_map)
        #     self._logger_level = (self.preset_name__level_map[self._logger_name])
        # else:
        #     self._logger_level = self._logger_level
        self._is_add_stream_handler = is_add_stream_handler
        self._do_not_use_color_handler = do_not_use_color_handler
        self._log_path = log_path
        self._log_filename = log_filename
        if error_log_filename is None and nb_log_config_default.AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE:
            error_log_filename = generate_error_file_name(log_filename)
        self._error_log_filename = error_log_filename
        self._log_file_size = log_file_size
        if log_file_handler_type not in (None, 1, 2, 3, 4, 5, 6, 7):
            raise ValueError("log_file_handler_type的值必须设置为 1 2 3 4 5 6 7这几个数字")
        self._log_file_handler_type = log_file_handler_type or nb_log_config_default.LOG_FILE_HANDLER_TYPE
        self._mongo_url = mongo_url
        self._is_add_elastic_handler = is_add_elastic_handler
        self._is_add_kafka_handler = is_add_kafka_handler
        self._ding_talk_token = ding_talk_token
        self._ding_talk_time_interval = ding_talk_time_interval
        self._mail_handler_config = mail_handler_config
        self._is_add_mail_handler = is_add_mail_handler
        self._is_use_loguru_stream_handler = nb_log_config_default.DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER if is_use_loguru_stream_handler is None \
            else is_use_loguru_stream_handler

        if isinstance(formatter_template, int):
            self._formatter = nb_log_config_default.FORMATTER_DICT[formatter_template]
        elif isinstance(formatter_template, logging.Formatter):
            self._formatter = formatter_template
        else:
            raise ValueError('设置的 formatter_template 不正确')

        self.logger.setLevel(self._logger_level)
        self.__add_handlers()
        # self.logger_name_list.append(self._logger_name)
        # self.logger_list.append(self.logger)
        return self.logger

    def get_logger_without_handlers(self):
        """返回一个不带hanlers的logger"""
        return self.logger

    # noinspection PyMethodMayBeStatic,PyMissingOrEmptyDocstring
    def look_over_all_handlers(self):
        very_nb_print(f'{self._logger_name}名字的日志的所有handlers是--> {self.logger.handlers}')

    def remove_all_handlers(self):
        # for hd in self.logger.handlers:
        #     self.logger.removeHandler(hd)
        self.logger.handlers = []

    def remove_handler_by_handler_class(self, handler_class: typing.Union[type, str]):
        """
        去掉指定类型的handler
        :param handler_class:logging.StreamHandler,ColorHandler,MongoHandler,ConcurrentRotatingFileHandler,MongoHandler,CompatibleSMTPSSLHandler的一种
        :return:
        """
        # if handler_class not in (
        #     logging.StreamHandler, ColorHandler, MongoHandler, ConcurrentRotatingFileHandler, MongoHandler,
        #     CompatibleSMTPSSLHandler, ElasticHandler, DingTalkHandler, KafkaHandler):
        #     raise TypeError('设置的handler类型不正确')
        all_handlers = copy.copy(self.logger.handlers)
        for handler in all_handlers:
            # if isinstance(handler, handler_class):
            if _get_hanlder_type(handler) == handler_class:
                self.logger.removeHandler(handler)  # noqa

    def __add_a_hanlder(self, handlerx: logging.Handler):
        handlerx.setLevel(self._logger_level)
        handlerx.setFormatter(self._formatter)
        self.logger.addHandler(handlerx)

    # def _judge_logger_has_handler_type(self, handler_type: typing.Union[type,str]):
    #     for hr in self.logger.handlers:
    #         if isinstance(hr, handler_type):
    #             return True

    def _judge_logger_has_not_handler_type(self, handler_type: typing.Union[type, str]):
        for hr in self.logger.handlers:
            if _get_hanlder_type(hr) == handler_type:
                return False
        return True

    def __add_file_hanlder(self, log_filename, is_error_level_file_handler):
        # REMIND 添加多进程安全切片的文件日志
        if all([self._log_path, log_filename]) and ((is_error_level_file_handler is False and self._judge_logger_has_not_handler_type(HANDLER_TYPE_FILE))
                                                    or (is_error_level_file_handler is True and self._judge_logger_has_not_handler_type(HANDLER_TYPE_ERROR_FILE))):
            if not os.path.exists(self._log_path):
                os.makedirs(self._log_path, exist_ok=True)
            log_file = str(os.path.join(self._log_path, log_filename))
            file_handler = None
            if self._log_file_handler_type == 1:
                if os_name == 'nt':
                    # 在win下使用这个ConcurrentRotatingFileHandler可以解决多进程安全切片，但性能损失惨重。
                    # 10进程各自写入10万条记录到同一个文件消耗15分钟。比不切片写入速度降低100倍。
                    from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos
                    file_handler = ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(log_file,
                                                                                            maxBytes=self._log_file_size * 1024 * 1024,
                                                                                            backupCount=nb_log_config_default.LOG_FILE_BACKUP_COUNT,
                                                                                            encoding="utf-8")


                elif os_name == 'posix':
                    # linux下可以使用ConcurrentRotatingFileHandler，进程安全的日志方式。
                    # 10进程各自写入10万条记录到同一个文件消耗100秒，还是比不切片写入速度降低10倍。因为每次检查切片大小和文件锁的原因。
                    from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandlerWithBufferInitiativeLinux
                    file_handler = ConcurrentRotatingFileHandlerWithBufferInitiativeLinux(log_file,
                                                                                          maxBytes=self._log_file_size * 1024 * 1024,
                                                                                          backupCount=nb_log_config_default.LOG_FILE_BACKUP_COUNT,
                                                                                          encoding="utf-8")

            elif self._log_file_handler_type == 4:
                file_handler = WatchedFileHandler(log_file)

            elif self._log_file_handler_type == 2:
                file_handler = ConcurrentDayRotatingFileHandler(log_filename, self._log_path, back_count=nb_log_config_default.LOG_FILE_BACKUP_COUNT)
            elif self._log_file_handler_type == 3:
                file_handler = FileHandler(log_file, mode='a', encoding='utf-8')
            elif self._log_file_handler_type == 5:
                from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandler
                file_handler = ConcurrentRotatingFileHandler(log_file,
                                                             maxBytes=self._log_file_size * 1024 * 1024,
                                                             backupCount=nb_log_config_default.LOG_FILE_BACKUP_COUNT,
                                                             encoding="utf-8")
            elif self._log_file_handler_type == 6:
                file_handler = BothDayAndSizeRotatingFileHandler(file_name=log_filename, log_path=self._log_path,
                                                                 back_count=nb_log_config_default.LOG_FILE_BACKUP_COUNT, max_bytes=self._log_file_size * 1024 * 1024)
            elif self._log_file_handler_type == 7:
                from nb_log.handlers_loguru import LoguruFileHandler
                logger_name_new = self._logger_name if not is_error_level_file_handler else f'{self._logger_name}_error'
                file_handler = LoguruFileHandler(logger_name=self._logger_name, sink=log_file)

            if is_error_level_file_handler:
                setattr(file_handler, MANUAL_HANLDER_TYPE, HANDLER_TYPE_ERROR_FILE)
                file_handler.setLevel(logging.ERROR)
            else:
                setattr(file_handler, MANUAL_HANLDER_TYPE, HANDLER_TYPE_FILE)
                file_handler.setLevel(self._logger_level)
            file_handler.setFormatter(self._formatter)
            self.logger.addHandler(file_handler)

    def __add_handlers(self):
        pass

        # REMIND 添加控制台日志
        if self._judge_logger_has_not_handler_type(HANDLER_TYPE_STREAM) and self._is_add_stream_handler:
            handler = ColorHandler() if not self._do_not_use_color_handler else logging.StreamHandler()  # 不使用streamhandler，使用自定义的彩色日志
            if self._is_use_loguru_stream_handler:
                from nb_log.handlers_loguru import LoguruStreamHandler
                handler = LoguruStreamHandler(self._logger_name, sink=sys.stdout)
            # handler = logging.StreamHandler()
            handler.setLevel(self._logger_level)
            setattr(handler, MANUAL_HANLDER_TYPE, HANDLER_TYPE_STREAM)
            self.__add_a_hanlder(handler)

        self.__add_file_hanlder(self._log_filename, is_error_level_file_handler=False)
        self.__add_file_hanlder(self._error_log_filename, is_error_level_file_handler=True)

        # REMIND 添加mongo日志。
        # if not self._judge_logger_has_handler_type(MongoHandler) and self._mongo_url:
        if self._mongo_url:
            from nb_log.handlers_more import MongoHandler
            if self._judge_logger_has_not_handler_type(MongoHandler):
                handler = MongoHandler(self._mongo_url)
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        if self._is_add_elastic_handler:
            """
            生产环境使用阿里云 oss日志，不使用这个。
            """
            from nb_log.handlers_more import ElasticHandler
            if self._judge_logger_has_not_handler_type(ElasticHandler):
                handler = ElasticHandler([nb_log_config_default.ELASTIC_HOST], nb_log_config_default.ELASTIC_PORT)
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        # REMIND 添加kafka日志。
        # if self._is_add_kafka_handler:
        if nb_log_config_default.RUN_ENV == 'test' and nb_log_config_default.ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT:
            from nb_log.handlers_more import KafkaHandler
            if self._judge_logger_has_not_handler_type(KafkaHandler):
                handler = KafkaHandler(nb_log_config_default.KAFKA_BOOTSTRAP_SERVERS, )
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        # REMIND 添加钉钉日志。
        if self._judge_logger_has_not_handler_type(DingTalkHandler) and self._ding_talk_token:
            handler = DingTalkHandler(self._ding_talk_token, self._ding_talk_time_interval)
            handler.setLevel(self._logger_level)
            self.__add_a_hanlder(handler)

        if self._judge_logger_has_not_handler_type(CompatibleSMTPSSLHandler) and self._is_add_mail_handler:
            handler = CompatibleSMTPSSLHandler(**self._mail_handler_config.get_dict())
            handler.setLevel(self._logger_level)
            self.__add_a_hanlder(handler)


@lru_cache()  # LogManager 本身也支持无限实例化
def get_logger(name: typing.Union[str, None], *, log_level_int: int = None, is_add_stream_handler=True,
               is_use_loguru_stream_handler: bool = None,
               do_not_use_color_handler=None, log_path=None,
               log_filename=None,
               error_log_filename=None,
               log_file_size: int = None,
               log_file_handler_type: int = None,
               mongo_url=None, is_add_elastic_handler=False, is_add_kafka_handler=False,
               ding_talk_token=None, ding_talk_time_interval=60,
               mail_handler_config: MailHandlerConfig = MailHandlerConfig(), is_add_mail_handler=False,
               formatter_template: typing.Union[int, logging.Formatter] = None) -> logging.Logger:
    """
    重写一遍，是为了更好的pycharm自动补全，所以不用**kwargs的写法。
    如果太喜欢函数调用了，可以使用这种.
    get_logger_and_add_handlers是LogManager类最常用的公有方法，其他方法使用场景的频率比较低，
    但如果要使用那些低频率功能，还是要亲自调用LogManger类，而不是仅仅只了解此函数的用法。
        :param name 日志命名空间，这个是最重要最难理解的一个入参，很多pythoner到现在还不知道name是什么作用。日志命名空间，意义非常非常非常重要，有些人到现在还不知道 logging.getLogger() 第一个入参的作用，太low了。不同的name的logger可以表现出不同的行为。
                例如让 aa命名空间的日志打印控制台并且写入到文件，并且只记录info级别以上，让 bb 命名空间的日志仅仅打印控制台，并且打印debug以上级别，
                这种就可以通过不同的日志命名空间做到。
        :param log_level_int: 日志输出级别，设置为 10 20 30 40 50，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，现在可以直接用10 20 30 40 50了，兼容了。
       :param is_add_stream_handler: 是否打印日志到控制台
       :param is_use_loguru_stream_handler  是否使用 loguru的控制台打印，如果为None，使用 nb_log_config.py的DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER 值。
       :param do_not_use_color_handler :是否禁止使用color彩色日志
       :param log_path: 设置存放日志的文件夹路径,如果不设置，则取nb_log_config.LOG_PATH，如果配置中也没指定则自动在代码所在磁盘的根目录创建/pythonlogs文件夹，
              非windwos下要注意账号权限问题(如果python没权限在根目录建/pythonlogs，则需要手动先创建好)
       :param log_filename: 日志文件名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
       :param error_log_filename :错误日志文件名字，如果文件名不为None，那么error级别以上日志自动写入到这个错误文件。
       :param log_file_size :日志大小，单位M，默认100M
       :param log_file_handler_type :这个值可以设置为1 2 3 4 5 6 7，1为使用多进程安全按日志文件大小切割的文件日志
              2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个日志
              3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题)
              4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
              5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
                这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
              6 为作者发明的高性能多进程安全，同时按大小和时间切割的文件日志handler
              7 为 loguru的 文件日志记录器
       :param mongo_url : mongodb的连接，为None时候不添加mongohandler
       :param is_add_elastic_handler: 是否记录到es中。
       :param is_add_kafka_handler: 日志是否发布到kafka。
       :param ding_talk_token:钉钉机器人token
       :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
       :param mail_handler_config : 邮件配置
       :param is_add_mail_handler :是否发邮件
       :param formatter_template :日志模板，如果为数字，则为nb_log_config.py字典formatter_dict的键对应的模板，
                                1为formatter_dict的详细模板，2为简要模板,5为最好模板。
                                如果为logging.Formatter对象，则直接使用用户传入的模板。
       :type log_level_int :int
       :type is_add_stream_handler :bool
       :type log_path :str
       :type log_filename :str
       :type mongo_url :str
       :type log_file_size :int
    """
    locals_copy = copy.copy(locals())
    locals_copy.pop('name')
    # print(locals_copy)
    return LogManager(name).get_logger_and_add_handlers(**locals_copy)


@lru_cache()
def get_logger_with_filehanlder(name: str) -> logging.Logger:
    """
    默认添加color handler  和 文件日志。
    :param name:
    :return:
    """
    return LogManager(name).get_logger_and_add_handlers(log_filename=name + '.log')


class LoggerLevelSetterMixin:
    # noinspection PyUnresolvedReferences
    def set_log_level(self, log_level=10):
        try:
            self.logger.setLevel(log_level)
        except AttributeError as e:
            very_nb_print(e)

        return self


class LoggerMixin(LoggerLevelSetterMixin):
    """
    主要是生成把类名作为日志命名空间的logger，方便被混入类直接使用self.logger，不需要手动实例化get_logger。
    """
    subclass_logger_dict = {}
    logger_extra_suffix = ''

    @property
    def logger_full_name(self):
        if self.logger_extra_suffix != '':
            return type(self).__name__ + '-' + self.logger_extra_suffix
        else:
            return type(self).__name__

    @property
    def logger(self) -> logging.Logger:
        logger_name_key = self.logger_full_name + '1'
        if logger_name_key not in self.subclass_logger_dict:
            logger_var = LogManager(self.logger_full_name).get_logger_and_add_handlers()
            self.subclass_logger_dict[logger_name_key] = logger_var
            return logger_var
        else:
            return self.subclass_logger_dict[logger_name_key]

    @property
    def logger_with_file(self) -> logging.Logger:
        logger_name_key = self.logger_full_name + '2'
        if logger_name_key not in self.subclass_logger_dict:
            logger_var = LogManager(self.logger_full_name).get_logger_and_add_handlers(
                log_filename=self.logger_full_name + '.log', )
            self.subclass_logger_dict[logger_name_key] = logger_var
            return logger_var
        else:
            return self.subclass_logger_dict[logger_name_key]


class LoggerMixinDefaultWithFileHandler(LoggerMixin):
    subclass_logger_dict = {}

    @property
    def logger(self):
        logger_name_key = self.logger_full_name + '3'
        if logger_name_key not in self.subclass_logger_dict:
            logger_var = LogManager(self.logger_full_name).get_logger_and_add_handlers(
                log_filename=self.logger_full_name + '.log', )
            self.subclass_logger_dict[logger_name_key] = logger_var
            return logger_var
        else:
            return self.subclass_logger_dict[logger_name_key]


FileLoggerMixin = LoggerMixinDefaultWithFileHandler


class MetaTypeLogger(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.logger = get_logger(name)


class MetaTypeFileLogger(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.logger = get_logger(name, log_filename=f'{name}.log')


def logger_catch(logger: logging.Logger, reraise: bool = True, show_trace_back=True):
    def _inner(f):
        def __inner(*args, **kwargs):
            try:
                res = f(*args, **kwargs)
            except Exception as e:
                logger.error(f'{f} , {args} ,{kwargs} , {e}', exc_info=show_trace_back)
                if reraise:
                    raise e
            else:
                return res

        return __inner

    return _inner


@lru_cache()
def build_exception_logger():
    print('_build_exception_logger')
    return get_logger('LoggedException', log_filename='exception.log', is_add_stream_handler=False)


class LoggedException(Exception):
    """
    抛出异常的同时,自动记录日志到日志文件中,这样就不需要每次都raise,并写日志日路,分两行来写了.
    try :
        1/0
    except Exception as e:
        raise LoggedException(message='有问题',)
    """

    def __init__(self, message: str, logger_obj=None, exc_info=True):
        """

        :param message:
        :param logger_obj: 传递logger对象,使用指定的logger来记录日志,那就log_filename不起作用
        :param exc_info: 日志是否记录仪详细报错堆栈
        """
        super().__init__('\n\n' + message)
        self._exc_info = exc_info
        self._logger_obj = logger_obj
        self._log_exception()

    def _log_exception(self):
        logger = self._logger_obj or build_exception_logger()
        logger.error(self, exc_info=self._exc_info)


def logged_raise(e: BaseException, logger_obj=None, exc_info=True):
    """
    try :
        1/0
    except Exception as e:
        logged_raise(ZeroDivisionError('0不能是被除数'))

    :param e:
    :param logger_obj:
    :param exc_info:
    :return:
    """
    logger = logger_obj or build_exception_logger()
    msg = str(e)
    if exc_info:
        traceback_list = traceback.format_tb(e.__traceback__)
        msg += '\n'.join(traceback_list)
    logger.error(f'\n\n {type(e)} {msg}', exc_info=exc_info)
    raise e

`````

--- **end of file: nb_log/log_manager.py** (project: nb_log) --- 

---


--- **start of file: nb_log/monkey_print.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/monkey_print.py`

#### 📝 Module Docstring

`````
不直接给print打补丁，自己重新赋值。
`````

#### 📦 Imports

- `import multiprocessing`
- `import os`
- `import sys`
- `import time`
- `import traceback`
- `from nb_log import nb_log_config_default`
- `from nb_log.rotate_file_writter import OsFileWritter`
- `import logging`

#### 🔧 Public Functions (9)

- `def stdout_write(msg: str)`
  - *Line: 21*

- `def stderr_write(msg: str)`
  - *Line: 27*
  - *打包exe运行或者做成windwos services 这些情况下情况下,sys.stderr是None,None.write会报错*

- `def nb_print(*args)`
  - *Line: 76*
  - **Docstring:**
  `````
  超流弊的print补丁
  :param x:
  :return:
  `````

- `def print_exception(etype, value, tb, limit = None, file = None, chain = True)`
  - *Line: 86*
  - **Docstring:**
  `````
  避免每行有两个可跳转的，导致第二个可跳转的不被ide识别。
  主要是针对print_exception，logging.exception里面会调用这个函数。
  
  # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断sys.stderr sys.stdout 以外的情况了，解决了，不需要用到p rint_exception。
  
  :param etype:
  :param value:
  :param tb:
  :param limit:
  :param file:
  :param chain:
  :return:
  `````

- `def patch_print()`
  - *Line: 114*
  - **Docstring:**
  `````
  Python有几个namespace，分别是
  
  locals
  
  globals
  
  builtin
  
  其中定义在函数内声明的变量属于locals，而模块内定义的函数属于globals。
  
  
  https://codeday.me/bug/20180929/266673.html   python – 为什么__builtins__既是模块又是dict
  
  :return:
  `````

- `def common_print(*args)`
  - *Line: 146*

- `def reverse_patch_print()`
  - *Line: 155*
  - **Docstring:**
  `````
  提供一个反猴子补丁，恢复print原状
  :return:
  `````

- `def is_main_process()`
  - *Line: 171*

- `def only_print_on_main_process(*args)`
  - *Line: 176*


---

`````python
# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/5/9 19:02
"""
不直接给print打补丁，自己重新赋值。

"""
import multiprocessing
import os
import sys
import time
import traceback
from nb_log import nb_log_config_default
# from nb_log.file_write import PrintFileWritter
from nb_log.rotate_file_writter import OsFileWritter

print_raw = print
WORD_COLOR = nb_log_config_default.WHITE_COLOR_CODE


def stdout_write(msg: str):
    if sys.stdout:
        sys.stdout.write(msg)
        sys.stdout.flush()


def stderr_write(msg: str):
    '''打包exe运行或者做成windwos services 这些情况下情况下,sys.stderr是None,None.write会报错'''
    if sys.stderr:
        sys.stderr.write(msg)
        sys.stderr.flush()
    else:
        stdout_write(msg)


print_wrtie_file_name = os.environ.get('PRINT_WRTIE_FILE_NAME', None) or nb_log_config_default.PRINT_WRTIE_FILE_NAME

print_file_writter = OsFileWritter(print_wrtie_file_name, log_path=nb_log_config_default.LOG_PATH,
                                   back_count=nb_log_config_default.LOG_FILE_BACKUP_COUNT, max_bytes=nb_log_config_default.LOG_FILE_SIZE * 1024 * 1024)


def _print_with_file_line(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2):
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    args_str = sep.join(args) + end
    # stdout_write(f'56:{file}')
    if file == sys.stderr:
        stderr_write(args_str)  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
        print_file_writter.write_2_file(args_str)
    elif file in [sys.stdout, None]:
        # 获取被调用函数在被调用时所处代码行数
        fra = sys._getframe(sys_getframe_n)
        line = fra.f_lineno
        file_name = fra.f_code.co_filename
        fun = fra.f_code.co_name
        now_str= time.strftime("%Y-%m-%d %H:%M:%S")
        # mtime = time.gmtime()
        # now_str = f'{mtime.tm_year}-{mtime.tm_mon}-{mtime.tm_mday} {mtime.tm_hour}:{mtime.tm_min}:{mtime.tm_sec}'
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        if nb_log_config_default.DEFAULUT_USE_COLOR_HANDLER:
            if nb_log_config_default.DISPLAY_BACKGROUD_COLOR_IN_CONSOLE:
                stdout_write(f'\033[0;34m{now_str}  "{file_name}:{line}" -{fun}-[print]-  \033[0;{WORD_COLOR};44m{args_str[:-1]}\033[0m \033[0m\n')  # 36  93 96 94
            else:
                stdout_write(
                    f'\033[0;{WORD_COLOR};34m{now_str}  "{file_name}:{line}" -{fun}-[print]-  {args_str[:-1]}  \033[0m\n')  # 36  93 96 94
            # sys.stdout.write(f'\033[0;30;44m"{file_name}:{line}"  {time.strftime("%H:%M:%S")}  {"".join(args)}\033[0m\n')
        else:
            stdout_write(
                f'{now_str}  "{file_name}:{line}"  -{fun}-[print]- {args_str} ')
        print_file_writter.write_2_file(f'{now_str}  "{file_name}:{line}" -[print]-{fun}- {args_str} ')  # 36  93 96 94
    else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
        print_raw(args_str, sep=sep, end=end, file=file)
        print_file_writter.write_2_file(args_str)


# noinspection PyProtectedMember,PyUnusedLocal,PyIncorrectDocstring,DuplicatedCode
def nb_print(*args, sep=' ', end='\n', file=None, flush=True):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    _print_with_file_line(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)


# noinspection PyPep8,PyUnusedLocal
def print_exception(etype, value, tb, limit=None, file=None, chain=True):
    """
    避免每行有两个可跳转的，导致第二个可跳转的不被ide识别。
    主要是针对print_exception，logging.exception里面会调用这个函数。

    # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断sys.stderr sys.stdout 以外的情况了，解决了，不需要用到p rint_exception。

    :param etype:
    :param value:
    :param tb:
    :param limit:
    :param file:
    :param chain:
    :return:
    """
    if file is None:
        file = sys.stderr
    for line in traceback.TracebackException(
        type(value), value, tb, limit=limit).format(chain=chain):
        # print(line, file=file, end="")
        if file != sys.stderr:
            stderr_write(f'{line} \n')
        else:
            stdout_write(f'{line} \n')


# print = nb_print

def patch_print():
    """
    Python有几个namespace，分别是

    locals

    globals

    builtin

    其中定义在函数内声明的变量属于locals，而模块内定义的函数属于globals。


    https://codeday.me/bug/20180929/266673.html   python – 为什么__builtins__既是模块又是dict

    :return:
    """
    if os.environ.get('has_patch_print'):
        return
    os.environ['has_patch_print'] = '1'
    try:
        __builtins__.print = nb_print
    except AttributeError:
        """
        <class 'AttributeError'>
        'dict' object has no attribute 'print'
        """
        # noinspection PyUnresolvedReferences
        __builtins__['print'] = nb_print
    # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断，解决了，不要加这个。


def common_print(*args, sep=' ', end='\n', file=None):
    args = (str(arg) for arg in args)
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        stderr_write(sep.join(args) + end)  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    else:
        stdout_write(sep.join(args) + end)


def reverse_patch_print():
    """
    提供一个反猴子补丁，恢复print原状
    :return:
    """
    # try:
    #     __builtins__.print = common_print
    # except AttributeError:
    #     __builtins__['print'] = common_print

    try:
        __builtins__.print = print_raw
    except AttributeError:
        __builtins__['print'] = print_raw


def is_main_process():
    return multiprocessing.process.current_process().name == 'MainProcess'


# noinspection DuplicatedCode
def only_print_on_main_process(*args, sep=' ', end='\n', file=None, flush=True):
    # 获取被调用函数在被调用时所处代码行数
    if is_main_process():
        _print_with_file_line(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)


if __name__ == '__main__':
    print('before patch')
    patch_print()
    print(0)
    nb_print(123, 'abc')
    print(456, 'def')
    print('http://www.baidu.com')

    reverse_patch_print()
    common_print('hi')

    import logging

    try:
        1 / 0
    except Exception as e:
        logging.exception(e)

`````

--- **end of file: nb_log/monkey_print.py** (project: nb_log) --- 

---


--- **start of file: nb_log/monkey_std_filter_words.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/monkey_std_filter_words.py`

#### 📦 Imports

- `import sys`
- `from nb_log import nb_log_config_default`

#### 🔧 Public Functions (1)

- `def patch_std_filter_words()`
  - *Line: 29*


---

`````python
import sys
from nb_log import nb_log_config_default


def _need_filter_print(msg: str):
    for strx in nb_log_config_default.FILTER_WORDS_PRINT:
        if strx in str(msg):
            return True  # 过滤掉需要屏蔽的打印
    return False


sys_stdout_write_raw = sys.stdout.write
sys_stderr_write_raw = sys.stderr.write


def _sys_stdout_write_monkey(msg: str):
    if _need_filter_print(msg):
        return
    else:
        sys_stdout_write_raw(msg)


def _sys_stderr_write_monkey(msg: str):
    if _need_filter_print(msg):
        return
    else:
        sys_stderr_write_raw(msg)

def patch_std_filter_words():
    sys.stdout.write = _sys_stdout_write_monkey  # 对 sys.stdout.write 打了猴子补丁。使得可以过滤包含指定字符串的消息。
    sys.stderr.write = _sys_stderr_write_monkey

`````

--- **end of file: nb_log/monkey_std_filter_words.py** (project: nb_log) --- 

---


--- **start of file: nb_log/monkey_sys_std.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/monkey_sys_std.py`

#### 📦 Imports

- `import atexit`
- `import os`
- `import sys`
- `import re`
- `import queue`
- `import threading`
- `import time`
- `from nb_log.rotate_file_writter import OsFileWritter`
- `from nb_log import nb_log_config_default`

#### 🏛️ Classes (1)

##### 📌 `class BulkStdout`
*Line: 25*

**Public Methods (2):**
- `def stdout(cls, msg)` `classmethod`
- `def start_bulk_stdout(cls)` `classmethod`

**Class Variables (3):**
- `q = queue.SimpleQueue()`
- `_lock = threading.Lock()`
- `_has_start_bulk_stdout = False`

#### 🔧 Public Functions (3)

- `def monkey_sys_stdout(msg)`
  - *Line: 66*

- `def monkey_sys_stderr(msg)`
  - *Line: 80*

- `def patch_sys_std()`
  - *Line: 90*


---

`````python
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

stdout_raw = getattr(sys.stdout,'write',None) # 打包時候,这个stdout是None,没有write方法
stderr_raw =  getattr(sys.stderr,'write',None)

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
                msg_str_all += str(cls.q.get())
            if msg_str_all and stdout_raw:
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
        if stdout_raw:
            try:
                stdout_raw(msg)
            except BrokenPipeError:
                pass
    msg_delete_color = dele_color_pattern.sub('', msg)
    std_writter.write_2_file(msg_delete_color)
    # std_writter.write_2_file(msg)


def monkey_sys_stderr(msg):
    if stderr_raw:
        try:
            stderr_raw(msg)
        except BrokenPipeError:
            pass
    msg_delete_color = dele_color_pattern.sub('', msg)
    std_writter.write_2_file(msg_delete_color)


def patch_sys_std():
    sys.stdout.write = monkey_sys_stdout
    sys.stderr.write = monkey_sys_stderr

`````

--- **end of file: nb_log/monkey_sys_std.py** (project: nb_log) --- 

---


--- **start of file: nb_log/nb_log_config_default.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/nb_log_config_default.py`

#### 📝 Module Docstring

`````
此文件nb_log_config.py是自动生成到python项目的根目录的,因为是自动生成到 sys.path[1]。
在这里面写的变量会覆盖此文件nb_log_config_default中的值。对nb_log包进行默认的配置。用户是无需修改nb_log安装包位置里面的配置文件的。

但最终配置方式是由get_logger_and_add_handlers方法的各种传参决定，如果方法相应的传参为None则使用这里面的配置。
`````

#### 📦 Imports

- `import sys`
- `import logging`
- `import os`
- `from pathlib import Path`
- `import socket`
- `from pythonjsonlogger.jsonlogger import JsonFormatter`

#### 🏛️ Classes (1)

##### 📌 `class JsonFormatterJumpAble(JsonFormatter)`
*Line: 109*

**Public Methods (1):**
- `def add_fields(self, log_record, record, message_dict)`

#### 🔧 Public Functions (1)

- `def get_host_ip()`
  - *Line: 91*


---

`````python
# coding=utf8
"""
此文件nb_log_config.py是自动生成到python项目的根目录的,因为是自动生成到 sys.path[1]。
在这里面写的变量会覆盖此文件nb_log_config_default中的值。对nb_log包进行默认的配置。用户是无需修改nb_log安装包位置里面的配置文件的。

但最终配置方式是由get_logger_and_add_handlers方法的各种传参决定，如果方法相应的传参为None则使用这里面的配置。
"""

"""
如果反对日志有各种彩色，可以设置 DEFAULUT_USE_COLOR_HANDLER = False
如果反对日志有块状背景彩色，可以设置 DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
如果想屏蔽nb_log包对怎么设置pycahrm的颜色的提示，可以设置 WARNING_PYCHARM_COLOR_SETINGS = False
如果想改变日志模板，可以设置 FORMATTER_KIND 参数，只带了7种模板，可以自定义添加喜欢的模板
LOG_PATH 配置文件日志的保存路径的文件夹。
"""
import sys
# noinspection PyUnresolvedReferences
import logging
import os
# noinspection PyUnresolvedReferences
from pathlib import Path  # noqa
import socket
from pythonjsonlogger.jsonlogger import JsonFormatter

# PRINT_WRTIE_FILE_NAME 是 黑科技配置,远超一般日志包所需要管辖的范畴,是nb_log 独门绝技.
# 项目中的print是否自动写入到文件中。值为None则不重定向print到文件中。 自动每天一个文件， 2023-06-30.my_proj.print,生成的文件位置在定义的LOG_PATH
# 如果你设置了环境变量，export PRINT_WRTIE_FILE_NAME="my_proj.print" (linux临时环境变量语法，windows语法自己百度这里不举例),那就优先使用环境变量中设置的文件名字，而不是nb_log_config.py中设置的名字
PRINT_WRTIE_FILE_NAME = os.environ.get("PRINT_WRTIE_FILE_NAME") or Path(sys.path[1]).name + '.print'

# SYS_STD_FILE_NAME 是 黑科技配置,远超一般日志包所需要管辖的范畴,是nb_log 独门绝技.
# 项目中的所有标准输出（不仅包括print，还包括了streamHandler日志）都写入到这个文件，为None将不把标准输出重定向到文件。自动每天一个文件， 2023-06-30.my_proj.std,生成的文件位置在定义的LOG_PATH
# 如果你设置了环境变量，export SYS_STD_FILE_NAME="my_proj.std"  (linux临时环境变量语法，windows语法自己百度这里不举例),那就优先使用环境变量中设置的文件名字，，而不是nb_log_config.py中设置的名字
# 这个相当于是 nohup 自动重定向所有屏幕输出流到一个nohup.out文件的功能了,这个是nb_log日志包的独有黑科技功能,logging 和loguru没这种功能.
# 相对如不同命名空间的logger写入到十几个不同的日志文件,这个SYS_STD_FILE_NAME把项目的所有日志单独重新汇总在一个文件.
SYS_STD_FILE_NAME = os.environ.get("SYS_STD_FILE_NAME") or Path(sys.path[1]).name + '.std'

USE_BULK_STDOUT_ON_WINDOWS = False  # 在win上是否每隔0.1秒批量stdout,win的io太差了

DEFAULUT_USE_COLOR_HANDLER = True  # 是否默认使用有彩的日志。
DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER = False  # 是否默认使用 loguru的控制台日志，而非是nb_log的ColorHandler
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True  # 在控制台是否显示彩色块状的日志。为False则不使用大块的背景颜色。
AUTO_PATCH_PRINT = True  # 是否自动打print的猴子补丁，如果打了猴子补丁，print自动变色和可点击跳转。

# 以下是屏蔽控制台所谓的烦人提示项,如果要关闭,先了解下这三个提示是什么,有的pythoner又菜又爱屏蔽提示,然后不知道为什么,这样的人太烦人了.
SHOW_PYCHARM_COLOR_SETINGS = True  # 有的人很反感启动代码时候提示教你怎么优化pycahrm控制台颜色，可以把这里设置为False  (怕提示颜色设置打扰你又不懂pycharm和python的颜色原理,就别抱怨颜色瞎眼)
SHOW_NB_LOG_LOGO = True  # 有的人反感启动代码时候打印nb_log 的logo图形,可以设置为False
SHOW_IMPORT_NB_LOG_CONFIG_PATH = True  # 是否打印读取的nb_log_config.py的文件位置.不懂pythonpath,不懂python导入模块机制的人,别屏蔽了,学习下  https://github.com/ydf0509/pythonpathdemo

WHITE_COLOR_CODE = 37  # 不同pycharm版本和主题,有的对白颜色生效的代号是97,有的是37, 这里可以设置 37和97, 如2023 pycahrm的console color,白颜色捕获的是97,如果这里写37,调节pycharm颜色没法调.

DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER = False  # 是否默认同时将日志记录到记log文件记事本中，就是用户不指定 log_filename的值，会自动写入日志命名空间.log文件中。
AUTO_WRITE_ERROR_LEVEL_TO_SEPARATE_FILE = False  # 自动把错误error级别以上日志写到单独的文件，根据log_filename名字自动生成错误文件日志名字。
LOG_FILE_SIZE = 1000  # 单位是M,每个文件的切片大小，超过多少后就自动切割
LOG_FILE_BACKUP_COUNT = 10  # 对同一个日志文件，默认最多备份几个文件，超过就删除了。

LOG_PATH = os.getenv("LOG_PATH")  # 优先从环境变量获取,启动代码之前可以 export LOG_PATH = '/你的日志目录/'
if not LOG_PATH:
    LOG_PATH = '/pythonlogs'  # 默认的日志文件夹,如果不写明磁盘名，则是项目代码所在磁盘的根目录下的/pythonlogs
    # LOG_PATH = Path(__file__).absolute().parent / Path("pythonlogs")   #这么配置就会自动在你项目的根目录下创建pythonlogs文件夹了并写入。
    if os.name == 'posix':  # linux非root用户和mac用户无法操作 /pythonlogs 文件夹，没有权限，默认修改为   home/[username]  下面了。例如你的linux用户名是  xiaomin，那么默认会创建并在 /home/xiaomin/pythonlogs文件夹下写入日志文件。
        home_path = os.environ.get("HOME", '/')  # 这个是获取linux系统的当前用户的主目录，不需要亲自设置
        LOG_PATH = Path(home_path) / Path('pythonlogs')  # linux mac 权限很严格，非root权限不能在/pythonlogs写入，修改一下默认值。
# print('LOG_PATH:',LOG_PATH)

LOG_FILE_HANDLER_TYPE = 6  # 1 2 3 4 5 6 7   # nb_log 的日志切割,全都追求多进程下切割正常.
"""
LOG_FILE_HANDLER_TYPE 这个值可以设置为 1 2 3 4 5 四种值，
1为使用多进程安全按日志文件大小切割的文件日志,这是本人实现的批量写入日志，减少操作文件锁次数，测试10进程快速写入文件，win上性能比第5种提高了100倍，linux提升5倍
2为多进程安全按天自动切割的文件日志，同一个文件，每天生成一个新的日志文件。日志文件名字后缀自动加上日期。
3为不自动切割的单个文件的日志(不切割文件就不会出现所谓进程安不安全的问题) 
4为 WatchedFileHandler，这个是需要在linux下才能使用，需要借助lograte外力进行日志文件的切割，多进程安全。
5 为第三方的concurrent_log_handler.ConcurrentRotatingFileHandler按日志文件大小切割的文件日志，
   这个是采用了文件锁，多进程安全切割，文件锁在linux上使用fcntl性能还行，win上使用win32con性能非常惨。按大小切割建议不要选第5个个filehandler而是选择第1个。
6 BothDayAndSizeRotatingFileHandler 使用本人完全彻底开发的，同时按照时间和大小切割，无论是文件的大小、还是时间达到了需要切割的条件就切割。
7 LoguruFileHandler ,使用知名的 loguru 包的文件日志记录器来写文件。
"""

LOG_LEVEL_FILTER = logging.DEBUG  # nb_log.get_logger不指定日志级别时候，默认日志级别，低于此级别的日志不记录了。例如设置为INFO，那么logger.debug的不会记录，只会记录logger.info以上级别的。
# 强烈不建议调高这里的级别为INFO，日志是有命名空间的，单独提高打印啰嗦的日志命名空间的日志级别就可以了，不要全局提高日志级别。
# https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c9.html#id2  文档9.5里面讲了几百次 python logging的命名空间的作用了，有些人到现在还不知道日志的name作用。

ROOT_LOGGER_LEVEL = logging.INFO # 根日志命名空间的日志级别，如果是INFO，没有添加handlers的其他命名空间的日志info及以上级别都会被记录，你可以亲自设置日志级别。
ROOT_LOGGER_FILENAME ='root.log' # 根日志命名空间的日志文件名字，默认是root.log。可以设置为None,则不记录到文件中。
ROOT_LOGGER_FILENAME_ERROR = 'root.error.log'  #  # 根日志命名空间的error级别以以上的日志单独文件名字。可以设置为None,则不另外生成一个error日志文件。

# 屏蔽的字符串显示，用 if in {打印信息} 来判断实现的,如果打印的消息中包括 FILTER_WORDS_PRINT 数组中的任何一个字符串，那么消息就不执行打印。
# 这个配置对 print 和 logger的控制台输出都生效。这个可以过滤某些啰嗦的print信息，也可以过滤同级别日志中的某些烦人的日志。可以用来过滤三方包中某些控制台打印。数组不要配置过多，否则有一丝丝影响性能会。
FILTER_WORDS_PRINT = []  # 例如， 你希望消息中包括阿弥陀佛 或者 包括善哉善哉 就不打印，那么可以设置  FILTER_WORDS_PRINT = ['阿弥陀佛','善哉善哉']


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
        log_record[f"{record.__dict__.get('pathname')}:{record.__dict__.get('lineno')}"] = ''  # 加个能点击跳转的字段。
        log_record['ip'] = computer_ip
        log_record['host_name'] = computer_name
        super().add_fields(log_record, record, message_dict)
        if 'for_segmentation_color' in log_record:
            del log_record['for_segmentation_color']


DING_TALK_TOKEN = '3dd0eexxxxxadab014bd604XXXXXXXXXXXX'  # 钉钉报警机器人

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
        '日志时间【%(asctime)s】 - 日志名称【%(name)s】 - 文件【%(filename)s】 - 第【%(lineno)d】行 - 日志等级【%(levelname)s】 - 日志信息【%(message)s】',
        "%Y-%m-%d %H:%M:%S"),
    2: logging.Formatter(
        '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),
    3: logging.Formatter(
        '%(asctime)s - %(name)s - 【 File "%(pathname)s", line %(lineno)d, in %(funcName)s 】 - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 一个模仿traceback异常的可跳转到打印日志地方的模板
    4: logging.Formatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
        "%Y-%m-%d %H:%M:%S"),  # 这个也支持日志跳转
    5: logging.Formatter(
        '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 我认为的最好的模板,推荐
    6: logging.Formatter('%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
                         "%Y-%m-%d %H:%M:%S"),
    7: logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # 一个只显示简短文件名和所处行数的日志模板

    8: JsonFormatterJumpAble('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s %(lineno)d  %(process)d %(thread)d', "%Y-%m-%d %H:%M:%S.%f",
                             json_ensure_ascii=False),  # 这个是json日志，方便elk采集分析.

    9: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 对5改进，带进程和线程显示的日志模板。
    10: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # 对7改进，带进程和线程显示的日志模板。
    11: logging.Formatter(
        f'%(asctime)s-({computer_ip},{computer_name})-[p%(process)d_t%(thread)d] - %(name)s - "%(filename)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"),  # 对7改进，带进程和线程显示的日志模板以及ip和主机名。
}

FORMATTER_KIND = 5  # 如果get_logger不指定日志模板，则默认选择第几个模板

`````

--- **end of file: nb_log/nb_log_config_default.py** (project: nb_log) --- 

---


--- **start of file: nb_log/root_logger.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/root_logger.py`

#### 📦 Imports

- `import logging`
- `import nb_log`
- `from nb_log import nb_log_config_default`


---

`````python
import logging

import nb_log
from nb_log import nb_log_config_default

_root_logger = logging.getLogger()
_root_handlers = _root_logger.handlers

new_hanlders = []

# if len(_root_logger.handlers):
#     hdr0 = _root_logger.handlers[0]
#     if type(hdr0) is logging.StreamHandler and not isinstance(hdr0,tuple(logging.StreamHandler.__subclasses__())):
#         # if hdr0.level == logging.NOTSET and hdr0.:
#         _root_logger.handlers.pop(0)
'''
有的人在使用nb_log之前，代码就已经运行了 logging.warning 这样的代码，需要先把之前的stream handler 删除掉，不然重复打印。
'''

for hdr in _root_handlers:
    if type(hdr) is logging.StreamHandler and not isinstance(hdr, tuple(logging.StreamHandler.__subclasses__())):
        print(f'drop root logger handler {hdr}')
        continue
    new_hanlders.append(hdr)

_root_logger.handlers = new_hanlders

# 根日志
root_logger = nb_log.get_logger(None,
                                log_filename=nb_log_config_default.ROOT_LOGGER_FILENAME,
                                error_log_filename=nb_log_config_default.ROOT_LOGGER_FILENAME_ERROR,
                                log_level_int=nb_log_config_default.ROOT_LOGGER_LEVEL)

`````

--- **end of file: nb_log/root_logger.py** (project: nb_log) --- 

---


--- **start of file: nb_log/rotate_file_writter.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/rotate_file_writter.py`

#### 📦 Imports

- `import atexit`
- `import multiprocessing`
- `import queue`
- `import threading`
- `import typing`
- `from pathlib import Path`
- `import time`
- `import os`

#### 🏛️ Classes (2)

##### 📌 `class FileWritter`
*Line: 18*

**🔧 Constructor (`__init__`):**
- `def __init__(self, file_name: str, log_path = '/pythonlogs', max_bytes = 1000 * 1000 * 1000, back_count = 10)`
  - **Parameters:**
    - `self`
    - `file_name: str`
    - `log_path = '/pythonlogs'`
    - `max_bytes = 1000 * 1000 * 1000`
    - `back_count = 10`

**Public Methods (1):**
- `def write_2_file(self, msg)`

**Properties (1):**
- `@property file_path`

**Class Variables (1):**
- `_lock = threading.RLock()`

##### 📌 `class BulkFileWritter`
*Line: 95*

**🔧 Constructor (`__init__`):**
- `def __init__(self, file_name: typing.Optional[str], log_path = '/pythonlogs', max_bytes = 1000 * 1000 * 1000, back_count = 10)`
  - **Parameters:**
    - `self`
    - `file_name: typing.Optional[str]`
    - `log_path = '/pythonlogs'`
    - `max_bytes = 1000 * 1000 * 1000`
    - `back_count = 10`

**Public Methods (3):**
- `def gen_file_key(log_path: str, file_name: str)` `staticmethod`
- `def write_2_file(self, msg)`
- `def start_bulk_write(cls)` `classmethod`

**Class Variables (6):**
- `_lock = threading.Lock()`
- `filename__queue_map = {}`
- `filename__options_map = {}`
- `filename__file_writter_map = {}`
- `_get_queue_lock = threading.Lock()`
- `_has_start_bulk_write = False`

#### 🔧 Public Functions (2)

- `def build_current_date_str()`
  - *Line: 14*

- `def tt()`
  - *Line: 175*


---

`````python
import atexit
import multiprocessing
import queue
import threading
import typing
from pathlib import Path
import time
import os


# from nb_log.simple_print import sprint as print  # 在此模块中不能print，print会写入文件，文件中print又写入文件，无限懵逼死循环。


def build_current_date_str():
    return time.strftime('%Y-%m-%d')


class FileWritter:
    _lock = threading.RLock()

    def __init__(self, file_name: str, log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000, back_count=10):
        self._max_bytes = max_bytes
        self._back_count = back_count
        self.need_write_2_file = True if file_name else False
        if self.need_write_2_file:
            self._file_name = file_name
            self.log_path = log_path
            if not Path(self.log_path).exists():
                print(f'自动创建日志文件夹 {log_path}')
                Path(self.log_path).mkdir(exist_ok=True)
            # self._open_file()
            self._first_has_open_file = False
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
            if self._first_has_open_file is False:
                self._first_has_open_file = True
                self._open_file()

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
                # print(f'删除 {f} ') # 这里不能print， stdout写入文件，写入文件时候print，死循环
                f.unlink()
            except (FileNotFoundError, PermissionError):
                pass


class BulkFileWritter:
    _lock = threading.Lock()

    filename__queue_map = {}
    filename__options_map = {}
    filename__file_writter_map = {}

    _get_queue_lock = threading.Lock()

    _has_start_bulk_write = False

    @staticmethod
    def gen_file_key(log_path: str,file_name: str):
        if not file_name:
            return ''
        return (Path(log_path) / Path(file_name)).absolute().as_posix()

    @classmethod
    def _get_queue(cls, file_key):
        if file_key not in cls.filename__queue_map:
            cls.filename__queue_map[file_key] = queue.SimpleQueue()
        return cls.filename__queue_map[file_key]

    @classmethod
    def _get_file_writter(cls, file_key):
        if file_key not in cls.filename__file_writter_map:
            fw = FileWritter(**cls.filename__options_map[file_key])
            cls.filename__file_writter_map[file_key] = fw
        return cls.filename__file_writter_map[file_key]

    def __init__(self, file_name: typing.Optional[str], log_path='/pythonlogs', max_bytes=1000 * 1000 * 1000, back_count=10):
        self.need_write_2_file = True if file_name else False
        self._file_name = file_name
        self._file_key = self.gen_file_key(log_path,file_name)
        if file_name:
            self.__class__.filename__options_map[self._file_key] = {
                'file_name': file_name,
                'log_path': log_path,
                'max_bytes': max_bytes,
                'back_count': back_count,
            }
            self.start_bulk_write()

    def write_2_file(self, msg):
        if self.need_write_2_file:
            with self._lock:
                self._get_queue(self._file_key).put(msg)

    @classmethod
    def _bulk_real_write(cls):
        with cls._lock:
            for file_key, queue in cls.filename__queue_map.items():
                msg_str_all = ''
                while not queue.empty():
                    msg_str_all += queue.get()
                if msg_str_all:
                    cls._get_file_writter(file_key).write_2_file(msg_str_all)

    @classmethod
    def _when_exit(cls):
        # print('结束')
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

OsFileWritter = FileWritter if os.name == 'posix' else BulkFileWritter


def tt():
    fw = OsFileWritter('test_file6.log', '/test_dir2', max_bytes=1000 * 100)
    t1 = time.time()
    for i in range(10000):
        # time.sleep(0.001)
        msg = f'yyy{str(i).zfill(5)}' * 4
        print(msg)
        fw.write_2_file(msg + '\n')
    print(time.time() - t1)


if __name__ == '__main__':
    multiprocessing.Process(target=tt).start()
    multiprocessing.Process(target=tt).start()
    # tt()

`````

--- **end of file: nb_log/rotate_file_writter.py** (project: nb_log) --- 

---


--- **start of file: nb_log/set_nb_log_config.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/set_nb_log_config.py`

#### 📝 Module Docstring

`````
使用覆盖的方式，做配置。
`````

#### 📦 Imports

- `import sys`
- `import importlib`
- `from pathlib import Path`
- `from nb_log import nb_log_config_default`
- `from nb_log.simple_print import sprint`
- `from shutil import copyfile`
- `import nb_log_config`

#### 🔧 Public Functions (3)

- `def show_nb_log_config()`
  - *Line: 30*

- `def use_config_form_nb_log_config_module()`
  - *Line: 40*
  - **Docstring:**
  `````
  自动读取配置。会优先读取启动脚本的目录的distributed_frame_config.py文件。没有则读取项目根目录下的distributed_frame_config.py
  :return:
  `````

- `def auto_creat_config_file_to_project_root_path()`
  - *Line: 64*
  - *:return:*


---

`````python
# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/4/11 0011 0:56
"""

使用覆盖的方式，做配置。
"""
import sys
import importlib
from pathlib import Path
from nb_log import nb_log_config_default
from nb_log.simple_print import sprint
from shutil import copyfile


def _get_show_import_nb_log_config_path():
    try:
        import nb_log_config
        return nb_log_config.SHOW_IMPORT_NB_LOG_CONFIG_PATH
    except Exception as e:
        return True


if _get_show_import_nb_log_config_path():
    cn_msg = f'当前项目的根目录是：\n {sys.path[1]}'
    en_msg = f'The project root directory is:\n {sys.path[1]}'
    sprint(en_msg, only_print_on_main_process=True)  # 如果获取的项目根目录不正确，请不要在python代码硬编码操作sys.path。pycahrm自动给项目根目录加了PYTHONPATh，如果是shell命令行运行python命令前脚本前先在会话中设置临时环境变量 export PYTHONPATH=项目根目录


def show_nb_log_config():
    cn_msg = '显示nb_log 包的默认的低优先级的配置参数'
    en_msg = 'Show the default low priority configuration parameters of the nb_log package'
    sprint(en_msg)
    for var_name in dir(nb_log_config_default):
        sprint(var_name, getattr(nb_log_config_default, ':', var_name))
    print('\n')


# noinspection PyProtectedMember
def use_config_form_nb_log_config_module():
    """
    自动读取配置。会优先读取启动脚本的目录的distributed_frame_config.py文件。没有则读取项目根目录下的distributed_frame_config.py
    :return:
    """
    try:
        m = importlib.import_module('nb_log_config')
        importlib.reload(m)  # 这行是防止用户在导入框架之前，写了 from nb_log_config import xx 这种，导致 m.__dict__.items() 不包括所有配置变量了。

        cn_msg1 = f'nb_log包 读取到\n "{m.__file__}:1" 文件里面的变量作为优先配置了\n'
        en_msg1 = f'nb_log has read the configuration variables in the \n "{m.__file__}:1" file as priority configuration\n'
        # nb_print(msg)
        if _get_show_import_nb_log_config_path():
            sprint(en_msg1, only_print_on_main_process=True)
        for var_namex, var_valuex in m.__dict__.items():
            if var_namex.isupper():
                setattr(nb_log_config_default, var_namex, var_valuex)
    except ModuleNotFoundError:
        auto_creat_config_file_to_project_root_path()
        cn_msg2 = f'''在你的项目根目录下生成了 \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" 的nb_log包的日志配置文件，快去看看并修改一些自定义配置吧'''
        en_msg2 = f'nb_log has created the configuration file \n "{Path(sys.path[1]) / Path("nb_log_config.py")}:1" in the project root directory.\n Please check and modify some custom configurations.'
        sprint(en_msg2, only_print_on_main_process=True)


def auto_creat_config_file_to_project_root_path():
    # print(Path(sys.path[1]).as_posix())
    # print((Path(__file__).parent.parent).absolute().as_posix())
    """
    :return:
    """
    if Path(sys.path[1]).as_posix() == Path(__file__).parent.parent.absolute().as_posix():
        pass
        cn_msg1 = f'不希望在本项目 {sys.path[1]} 里面创建 nb_log_config.py'
        en_msg1 = f'It is not expected to create the nb_log_config.py file in this project {sys.path[1]}'
        sprint(en_msg1, only_print_on_main_process=True)
        return
    # noinspection PyPep8
    """
        如果没设置PYTHONPATH，sys.path会这样，取第一个就会报错
        ['', '/data/miniconda3dir/inner/envs/mtfy/lib/python36.zip', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/lib-dynload', '/root/.local/lib/python3.6/site-packages', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/site-packages']
        
        ['', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\python36.zip', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\DLLs', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\multiprocessing_log_manager-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pyinstaller-3.4-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pywin32_ctypes-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\altgraph-0.16.1-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\macholib-1.11-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pefile-2019.4.18-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\Pythonwin']
        """
    if '/lib/python' in sys.path[1] or r'\lib\python' in sys.path[1] or '.zip' in sys.path[1]:
        cn_err_msg2 = '''如果用pycahrm启动，默认不需要你手动亲自设置PYTHONPATH，如果你是cmd或者shell中直接敲击python xx.py 来运行，
                               报现在这个错误，你现在肯定是没有设置PYTHONPATH环境变量，不要设置永久环境变量，设置临时会话环境变量就行，
                               windows设置  set PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               linux设置    export PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               要是连PYTHONPATH这个知识点都不知道，那就要google 百度去学习PYTHONPATH作用了，非常重要非常好用，
                               不知道PYTHONPATH作用的人，在深层级文件夹作为运行起点导入外层目录的包的时候，如果把深层级文件作为python的执行文件起点，经常需要到处很low的手写 sys.path.insert硬编码，这种方式写代码太low了。
                               知道PYTHONPATH的人无论项目有多少层级的文件夹，无论是多深层级文件夹导入外层文件夹，代码里面永久都不需要出现手动硬编码操纵sys.path.append
                               
                               懂PYTHONPATH 的重要性和妙用见： https://github.com/ydf0509/pythonpathdemo
                               '''
        en_err_msg2 = f'''If you use pycahrm to start the project, you do not need to manually set the PYTHONPATH environment variable by default.
                               If you run the project directly in the cmd or shell, you will get the current error.
                               You must not set the PYTHONPATH environment variable permanently, but set it temporarily in the session environment variable.
                               Windows setting: set PYTHONPATH=your current python project root directory, then run your python command.
                               Linux setting: export PYTHONPATH=your current python project root directory, then run your python command.
                               If you do not know the PYTHONPATH concept, you should google or baidu to learn about its importance and usage.
                               If you do not know the PYTHONPATH concept, you will often need to write very low-level code to manually manipulate sys.path.append.
                               Understanding the importance and usage of PYTHONPATH is very important and useful.
                               See: https://github.com/ydf0509/pythonpathdemo for more details.
                               '''
        raise EnvironmentError(en_err_msg2)
    # with (Path(sys.path[1]) / Path('nb_log_config.py')).open(mode='w', encoding='utf8') as f:
    #     f.write(config_file_content)
    copyfile(Path(__file__).parent / Path('nb_log_config_default.py'), Path(sys.path[1]) / Path('nb_log_config.py'))
    cn_msg3 = f'''在  {Path(sys.path[1])} 目录下自动生成了一个文件， 请刷新文件夹查看或修改 \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" 文件'''
    en_msg3 = f'''A file has been automatically generated in the {Path(sys.path[1])} directory. Please refresh the folder to view or modify \n "{Path(sys.path[1]) / Path('nb_log_config.py')}:1" file'''
    sprint(en_msg3)


use_config_form_nb_log_config_module()

`````

--- **end of file: nb_log/set_nb_log_config.py** (project: nb_log) --- 

---


--- **start of file: nb_log/simple_print.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/simple_print.py`

#### 📦 Imports

- `import atexit`
- `import os`
- `import queue`
- `import sys`
- `import threading`
- `import time`
- `import multiprocessing`

#### 🔧 Public Functions (3)

- `def stdout_write(msg: str)`
  - *Line: 13*

- `def stderr_write(msg: str)`
  - *Line: 19*

- `def sprint(*args)`
  - *Line: 47*


---

`````python
import atexit
import os
import queue
import sys
import threading
import time
import multiprocessing

print_raw = print
WORD_COLOR = 37


def stdout_write(msg: str):
    if sys.stdout:
        sys.stdout.write(msg)
        sys.stdout.flush()


def stderr_write(msg: str):
    if sys.stderr:
        sys.stderr.write(msg)
        sys.stderr.flush()
    else:
        stdout_write(msg)



def _sprint(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2, ):
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    args_str = sep.join(args) + end
    # stdout_write(f'56:{file}')
    if file == sys.stderr:
        stderr_write(args_str)  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    elif file in [sys.stdout, None]:
        # 获取被调用函数在被调用时所处代码行数
        fra = sys._getframe(sys_getframe_n)
        line = fra.f_lineno
        file_name = fra.f_code.co_filename
        fun = fra.f_code.co_name
        # sys.stdout.write(f'"{__file__}:{sys._getframe().f_lineno}"    {x}\n')
        msg = f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}"  - {fun} - {args_str}'
        stdout_write(msg)
    else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
        print_raw(args_str, sep=sep, end=end, file=file)


def sprint(*args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2, only_print_on_main_process=False):
    if only_print_on_main_process:
        if multiprocessing.process.current_process().name == 'MainProcess':
            _sprint(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=2)
    else:
        _sprint(*args, sep=sep, end=end, file=file, flush=flush, sys_getframe_n=sys_getframe_n)


if __name__ == '__main__':
    str1 = 'O(∩_∩)O哈哈' * 40
    t1 = time.time()
    for i in range(10000):
        sprint(str1)

    print(time.time() - t1)

`````

--- **end of file: nb_log/simple_print.py** (project: nb_log) --- 

---


--- **start of file: nb_log/__init__.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/__init__.py`

#### 📦 Imports

- `import logging`
- `import warnings`
- `import nb_log.add_python_executable_dir_to_path_env`
- `from nb_log.set_nb_log_config import use_config_form_nb_log_config_module`
- `from nb_log import nb_log_config_default`
- `from nb_log.monkey_sys_std import patch_sys_std`
- `from nb_log.monkey_sys_std import stderr_raw`
- `from nb_log.monkey_sys_std import stdout_raw`
- `from nb_log.monkey_std_filter_words import patch_std_filter_words`
- `from nb_log.monkey_print import nb_print`
- `from nb_log.monkey_print import patch_print`
- `from nb_log.monkey_print import reverse_patch_print`
- `from nb_log.monkey_print import stdout_write`
- `from nb_log.monkey_print import stderr_write`
- `from nb_log.monkey_print import print_raw`
- `from nb_log.monkey_print import is_main_process`
- `from nb_log.monkey_print import only_print_on_main_process`
- `from nb_log.helpers import generate_error_file_name`
- `from nb_log import handlers`
- `from nb_log.log_manager import LogManager`
- `from nb_log.log_manager import LoggerLevelSetterMixin`
- `from nb_log.log_manager import LoggerMixin`
- `from nb_log.log_manager import LoggerMixinDefaultWithFileHandler`
- `from nb_log.log_manager import FileLoggerMixin`
- `from nb_log.log_manager import MetaTypeLogger`
- `from nb_log.log_manager import MetaTypeFileLogger`
- `from nb_log.log_manager import get_logger`
- `from nb_log.log_manager import get_logger_with_filehanlder`
- `from nb_log.loggers_imp.compatible_logger import CompatibleLogger`
- `from nb_log import global_except_hook`
- `from nb_log.exception_auto_log import LogException`
- `from nb_log.root_logger import root_logger`
- `from nb_log.capture_warnings import capture_warnings_with_frequency_control`
- `from nb_log.direct_logger import debug`
- `from nb_log.direct_logger import info`
- `from nb_log.direct_logger import warning`
- `from nb_log.direct_logger import error`
- `from nb_log.direct_logger import exception`
- `from nb_log.direct_logger import critical`


---

`````python
import logging
import warnings
import nb_log.add_python_executable_dir_to_path_env
from nb_log.set_nb_log_config import use_config_form_nb_log_config_module
from nb_log import nb_log_config_default

from nb_log.monkey_sys_std import patch_sys_std,stderr_raw,stdout_raw
if nb_log_config_default.SYS_STD_FILE_NAME:
    patch_sys_std()

from nb_log.monkey_std_filter_words import patch_std_filter_words
if nb_log_config_default.FILTER_WORDS_PRINT:
    patch_std_filter_words()

from nb_log.monkey_print import nb_print, patch_print, reverse_patch_print, stdout_write, stderr_write, print_raw, is_main_process, only_print_on_main_process
if nb_log_config_default.AUTO_PATCH_PRINT:
    patch_print()



from nb_log.helpers import generate_error_file_name
from nb_log import handlers
from nb_log.log_manager import (LogManager, LoggerLevelSetterMixin, LoggerMixin, LoggerMixinDefaultWithFileHandler,FileLoggerMixin,
                                MetaTypeLogger,MetaTypeFileLogger,
                                get_logger, get_logger_with_filehanlder,
                                )
from nb_log.loggers_imp.compatible_logger import CompatibleLogger

simple_logger = get_logger('simple')
default_logger = LogManager('default').get_logger_and_add_handlers(do_not_use_color_handler=True, )
defaul_logger = default_logger # 兼容下defaul_logger错误的拼写，有的人把funboost版本固定死了，但nb_log版本却不固定，删除defaul_logger会导致funboost报错
default_file_logger = LogManager('default_file_logger').get_logger_and_add_handlers(log_filename='default_file_logger.log')

logger_dingtalk_common = LogManager('钉钉通用报警提示').get_logger_and_add_handlers(
    ding_talk_token=nb_log_config_default.DING_TALK_TOKEN,
    log_filename='dingding_common.log')

from nb_log import global_except_hook
from nb_log.exception_auto_log import LogException

# warnings.simplefilter('always')  # 避免维护 sys.__dict__['__warningregistry__'] 字典,由 warning.warn 引起的内存泄漏
# logging.captureWarnings(True) # 将warning.warn的sys.stderr 转化成日志.
# get_logger('',log_level_int=logging.WARNING,log_filename='root.log')  # py.warnings

from nb_log.root_logger import root_logger


from nb_log.capture_warnings import capture_warnings_with_frequency_control

from nb_log.direct_logger import debug,info,warning,error,exception,critical

if nb_log_config_default.SHOW_NB_LOG_LOGO:
    only_print_on_main_process('\033[0m' + r"""
    
    .__   __. .______           __        ______     _______ 
    |  \ |  | |   _  \         |  |      /  __  \   /  _____|
    |   \|  | |  |_)  |  ______|  |     |  |  |  | |  |  __  
    |  . `  | |   _  <  |______|  |     |  |  |  | |  | |_ | 
    |  |\   | |  |_)  |        |  `----.|  `--'  | |  |__| | 
    |__| \__| |______/         |_______| \______/   \______|      
    
         """ + '\033[0m')

if nb_log_config_default.SHOW_PYCHARM_COLOR_SETINGS:
    cn_msg =   """\033[0m
        1)使用pycharm时候，强烈建议按下面的重新自定义设置pycharm的console里面的主题颜色，否则颜色显示瞎眼，代码里面规定的颜色只是大概的红黄蓝绿。在不同的ide软件和主题、字体下是不同的显示效果，需要用户自己设置。
        设置方式为 打开pycharm的 file -> settings -> Editor -> Color Scheme -> Console Colors 选择monokai，点击展开 ANSI colors，
        并重新修改自定义7个颜色，设置Blue为 0454F3 ，Cyan为 06F0F6 ，Green 为 13FC02 ，Magenta为 ff1cd5 ,red为 F80606 ，yellow为 EAFA04 ，gray 为 FFFFFF ，white 为 FFFFFF 。
        不同版本的pycahrm或主题或ide，可以根据控制台根据实际显示设置。

        2)使用xshell或finashell工具连接linux也可以自定义主题颜色，默认使用shell连接工具的颜色也可以。

        颜色效果如连接 https://ibb.co/qRssXTr

        在当前项目根目录的 nb_log_config.py 中可以修改当get_logger方法不传参时后的默认日志行为。

        nb_log文档 https://nb-log-doc.readthedocs.io/zh_CN/latest/

        为什么要设置pycharm终端颜色，解释为什么\\033不能决定最终颜色 https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c1.html#c
        \033[0m

        """
    en_msg = """\033[0m
        1)When using PyCharm, it is strongly recommended to re-customize the theme colors in PyCharm's console as follows, otherwise the color display may be harsh on the eyes. The colors specified in the code are just approximate red, yellow, blue, and green. The display effect varies across different IDE software, themes, and fonts, so users need to set them up themselves.
        The setup method is: Open PyCharm -> File -> Settings -> Editor -> Color Scheme -> Console Colors, select monokai, click to expand ANSI colors,
        and re-modify 7 custom colors: set Blue to 0454F3, Cyan to 06F0F6, Green to 13FC02, Magenta to ff1cd5, red to F80606, yellow to EAFA04, gray to FFFFFF, and white to FFFFFF.
        Different versions of PyCharm, themes, or IDEs can be set according to the actual console display.

        2)When using tools like xshell or finashell to connect to Linux, you can also customize the theme colors, or use the default colors of the shell connection tool.

        Color effect as shown at https://ibb.co/qRssXTr

        You can modify the default logging behavior when the get_logger method is called without parameters in nb_log_config.py at the root directory of the current project.

        nb_log documentation https://nb-log-doc.readthedocs.io/zh_CN/latest/

        Why set PyCharm terminal colors, explaining why \033 cannot determine the final color https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c1.html#c
        \033[0m
        """
    only_print_on_main_process(en_msg)
`````

--- **end of file: nb_log/__init__.py** (project: nb_log) --- 

---


--- **start of file: nb_log/loggers_imp/compatible_logger.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/loggers_imp/compatible_logger.py`

#### 📦 Imports

- `import sys`
- `import os`
- `import traceback`
- `import io`
- `import logging`
- `from logging import _srcfile`

#### 🏛️ Classes (1)

##### 📌 `class CompatibleLogger(logging.Logger)`
*Line: 39*

**Docstring:**
`````
写 CompatibleLogger 是在python3.7测试的，python3.9以后官方已经加了stacklevel入参。
20230705 现在经过github cpython的源码核实，在python3.9版本中
def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False,
         stacklevel=1):

def findCaller(self, stack_info=False, stacklevel=1):

python3.9以上用户可以传递 stacklevel 了，本NbLogger是适配python3.6 3.7 3.8版本, Nblogger 的 sys_getframe_n 入参就是 stacklevel 的意义。
说明我的思维和python官方人员想到一起去了，3.9以后的logging包debug ingo error等 支持修改查找调用堆栈的深度层级，防止用户封装了debug info warnring 等后，日志模板获取的 文件名 行号是错误深度层级的。。
`````

**Public Methods (1):**
- `def findCaller(self, stack_info = False, sys_getframe_n = 2)`
  - **Docstring:**
  `````
  主要是改了这个，使得文件和行号变成用户本身的打印日志地方，而不是封装日志的地方。
  :param stack_info:
  :param sys_getframe_n: 新增的入参。
  :return:
  `````


---

`````python
import sys
import os
import traceback
import io
import logging
from logging import _srcfile

'''
新增的 NbLogger 类，继承自内置 logging.Logger，
主要作用是可以改变 sys._getframe 深度，  
目的是 如果用户自己使用代码模式封装了日志类，在自己的类中又多此一举实现 debug info warning error critical 打印日志的方法， 
用户在使用 用户自己类.debug() 时候 ，导致记录日志的行号是用户封装这几个方法的地方，而不是实际打印日志的地方，不方便定位日志是从哪里打印的。
'''

'''
from nb_log import get_logger


class 废物日志类:
    def __init__(self,name):
        self.logger = get_logger(name, _log_filename='废物日志.log')

    def debug(self, msg):
        self.logger.debug(msg, extra={'sys_getframe_n': 3})  # 第 x1 行

    def info(self, msg):
        self.logger.info(msg, extra={'sys_getframe_n': 3})  # 第 x2 行


废物日志类('命名空间1').info('啊啊啊啊')  # 第y行
'''

'''
有的人手痒，非要封装nb_log,那么封装时候调用原生日志的 info() 务必要传入  extra={'sys_getframe_n': 3}
如果你不传递 extra={'sys_getframe_n': 3} ，那么 废物日志类().info('啊啊啊啊') ，显示是第 x2 行打印的日志，而不是第 y行打印的日志。
'''


class CompatibleLogger(logging.Logger):

    """
    写 CompatibleLogger 是在python3.7测试的，python3.9以后官方已经加了stacklevel入参。
    20230705 现在经过github cpython的源码核实，在python3.9版本中
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False,
             stacklevel=1):

    def findCaller(self, stack_info=False, stacklevel=1):

    python3.9以上用户可以传递 stacklevel 了，本NbLogger是适配python3.6 3.7 3.8版本, Nblogger 的 sys_getframe_n 入参就是 stacklevel 的意义。
    说明我的思维和python官方人员想到一起去了，3.9以后的logging包debug ingo error等 支持修改查找调用堆栈的深度层级，防止用户封装了debug info warnring 等后，日志模板获取的 文件名 行号是错误深度层级的。。

    """
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False,**kwargs):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """

        sys_getframe_n =2
        if extra and 'sys_getframe_n' in extra:
            sys_getframe_n = extra['sys_getframe_n']
            extra.pop('sys_getframe_n')
        sinfo = None
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info,sys_getframe_n)  # 这个改了，加了个入参。
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                 exc_info, func, extra, sinfo)
        self.handle(record)

    def findCaller(self, stack_info=False,sys_getframe_n =2):
        """
        主要是改了这个，使得文件和行号变成用户本身的打印日志地方，而不是封装日志的地方。
        :param stack_info:
        :param sys_getframe_n: 新增的入参。
        :return:
        """
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = sys._getframe(sys_getframe_n)   # 这行改了。
        # f = sys._getframe(3)
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


`````

--- **end of file: nb_log/loggers_imp/compatible_logger.py** (project: nb_log) --- 

---


--- **start of file: nb_log/loggers_imp/__init__.py** (project: nb_log) --- 


### 📄 Python File Metadata: `nb_log/loggers_imp/__init__.py`


---

`````python

`````

--- **end of file: nb_log/loggers_imp/__init__.py** (project: nb_log) --- 

---


