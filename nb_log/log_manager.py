# coding=utf8
# noinspection SpellCheckingInspection
"""
Log management module supporting console output, rotating file output, MongoDB, email, DingTalk bot, Elasticsearch, and Kafka.
Uses the builder pattern to create and return native logging.Logger objects with various useful handlers attached.
Highly compatible and extensible - follow the observer pattern examples to add custom handlers.

Usage: logger = LogManager('logger_name').get_and_add_handlers(log_level_int=1, is_add_stream_handler=True,
 log_path=None, _log_filename=None, log_file_size=10,mongo_url=None,formatter_template=2)

ConcurrentRotatingFileHandler from concurrent_log_handler solves the multi-process file rotation issues
in the built-in RotatingFileHandler. Works correctly on both Windows and Linux.

Key features:
1. ColorHandler replaces StreamHandler to display 5 color-coded log levels for easy severity identification.
2. Multiple handler types: email, MongoDB, stream, and file.
3. Supports clickable log navigation in PyCharm to jump to the corresponding source line.
4. Prevents duplicate handlers of the same type on the same logger namespace - no manual deduplication needed.
5. Improved file logging performance: batch-writes buffered messages every second,
   achieving 100x speedup on Windows and 10x on Linux for multi-process safe file rotation.
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
def revision_call_handlers(self, record):  # Monkey-patch for the logging module to prevent parent namespace handlers from duplicating log output.
    """
    Important: This ensures that adding the same handler type to both a logger and its parent won't cause duplicate output.
    For example, adding a StreamHandler to both 'a' and 'a.b' namespaces would normally print 'a.b' logs twice.
    Example:

    import logging

    logger1 = logging.getLogger('a')
    logger1.addHandler(logging.StreamHandler())

    logger2 = logging.getLogger('a.b')
    logger2.addHandler(logging.StreamHandler())

    logger2.error(666)

    Without this patch, 666 would be printed twice because the parent namespace 'a' also has a StreamHandler.

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
            # if hdlr_type == logging.StreamHandler:  # REMIND Many handlers inherit from StreamHandler (including FileHandler), so direct type check would cause logic errors.
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
def revision_add_handler(self, hdlr):  # Prevent adding duplicate handler types to the same logger at the source.
    """
    Add the specified handler to this logger.
    """
    # logging._acquireLock()  # noqa
    """ Original implementation:
    if not (hdlr in self.handlers):
        self.handlers.append(hdlr)
    """
    with _lock:
        hdlrx_type_set = set()
        for hdlrx in self.handlers:
            hdlrx_type = _get_hanlder_type(hdlrx)
            # if hdlrx_type == logging.StreamHandler:  # REMIND Many handlers inherit from StreamHandler (including FileHandler), so direct type check would cause logic errors.
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
        very_nb_print(f'Logger namespace {self.name} is locked to level {level2}, subsequent attempt to change to level {level} is ignored')
    self.level = _checkLevel(level2)
    if sys.version_info.minor >= 7:  # python3.6 doesn't have _clear_cache method
        self.manager._clear_cache()


logging.Logger.callHandlers = revision_call_handlers  # Monkey-patch
logging.Logger.addHandler = revision_add_handler  # Monkey-patch
logging.Logger.setLevel = revision_setLevel  # Monkey-patch


# noinspection PyShadowingBuiltins
# print = very_nb_print


class _Undefind:
    pass


undefind = _Undefind()


# noinspection DuplicatedCode
class DataClassBase:
    """
    A class-based data container.
    Provides better IDE auto-completion compared to plain dictionaries.
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
    subject: str = 'Project Email Log Alert'
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


LOG_LEVEL_LIST = [logging.NOTSET,logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]  # i.e. 0 10 20 30 40 50


def check_log_level(log_level: int):
    if log_level not in LOG_LEVEL_LIST:
        raise ValueError(f'Invalid log level: {log_level}. Must be one of {LOG_LEVEL_LIST}')


# noinspection PyMissingOrEmptyDocstring,PyPep8
class LogManager(object):
    """
    A log manager class for creating loggers and adding handlers.
    Supports console output, file logging, MongoDB, email, and more.
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
        :param logger_name: Logger name. When None, operates on the root namespace. Avoid using None unless you fully understand the implications.
        """
        if logger_name in (None, '',) and multiprocessing.process.current_process().name == 'MainProcess':
            pass
            # very_nb_print('Setting logger_name to None or empty string both operate on the root namespace. '
            #               'This affects all other loggers. Make sure you understand the logging name concept.')
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
        Pre-set and lock a log level for this namespace. Once set, subsequent level changes are ignored.
        Useful for dynamically initialized loggers where setting the level after creation is inconvenient.
        :param log_level_int: e.g. logging.DEBUG, logging.INFO, etc.
        :return:
        """
        check_log_level(log_level_int)
        self.preset_name__level_map[self._logger_name or 'root'] = log_level_int
        self.logger.setLevel(log_level_int)

    def prevent_add_handlers(self):
        """Prevent any further handlers from being added to this namespace"""

        def _add_handler(handler: logging.Handler):
            pass

        self.logger.addHandler = _add_handler

    # The * forces keyword-only arguments to prevent positional arg issues when new parameters are added in the future.
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
       :param log_level_int: Log output level. Use 10/20/30/40/50 corresponding to DEBUG/INFO/WARNING/ERROR/CRITICAL.
       :param is_add_stream_handler: Whether to print logs to console.
       :param is_use_loguru_stream_handler: Whether to use loguru's console handler. If None, uses DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER from config.
       :param do_not_use_color_handler: Whether to disable colored log output.
       :param log_path: Directory for log files. Defaults to nb_log_config.LOG_PATH, or /pythonlogs if not configured.
              On non-Windows systems, ensure proper directory permissions.
       :param log_filename: Log filename. Logs are written to file only when both log_path and log_filename are not None.
       :param error_log_filename: Error log filename. If not None, ERROR level and above are written to this separate file.
       :param log_file_size: Max log file size in MB. Default 100MB.
       :param log_file_handler_type: File handler type (1-7):
              1 - Multi-process safe size-based rotation with batch writing (recommended for size-based rotation)
              2 - Multi-process safe daily rotation
              3 - Single file without rotation
              4 - WatchedFileHandler (Linux only, requires external logrotate)
              5 - ConcurrentRotatingFileHandler with file locks (poor performance on Windows)
              6 - High-performance rotation by both time and size
              7 - Loguru file handler
       :param mongo_url: MongoDB connection URL. None to skip MongoDB handler.
       :param is_add_elastic_handler: Whether to log to Elasticsearch.
       :param is_add_kafka_handler: Whether to publish logs to Kafka.
       :param ding_talk_token: DingTalk bot token.
       :param ding_talk_time_interval: Min interval between DingTalk messages in seconds.
       :param mail_handler_config: Email handler configuration.
       :param is_add_mail_handler: Whether to send log emails.
       :param formatter_template: Log format template. If int, uses the corresponding template from FORMATTER_DICT.
                                If a logging.Formatter object, uses it directly.
       :type log_level_int: int
       :type is_add_stream_handler: bool
       :type log_path: str
       :type log_filename: str
       :type mongo_url: str
       :type log_file_size: int
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
            raise ValueError("log_file_handler_type must be one of 1, 2, 3, 4, 5, 6, 7")
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
            raise ValueError('Invalid formatter_template: must be an int or a logging.Formatter instance')

        self.logger.setLevel(self._logger_level)
        self.__add_handlers()
        # self.logger_name_list.append(self._logger_name)
        # self.logger_list.append(self.logger)
        return self.logger

    def get_logger_without_handlers(self):
        """Return a logger without any handlers attached"""
        return self.logger

    # noinspection PyMethodMayBeStatic,PyMissingOrEmptyDocstring
    def look_over_all_handlers(self):
        very_nb_print(f'All handlers for logger "{self._logger_name}": {self.logger.handlers}')

    def remove_all_handlers(self):
        # for hd in self.logger.handlers:
        #     self.logger.removeHandler(hd)
        self.logger.handlers = []

    def remove_handler_by_handler_class(self, handler_class: typing.Union[type, str]):
        """
        Remove handlers of the specified type.
        :param handler_class: One of logging.StreamHandler, ColorHandler, MongoHandler, ConcurrentRotatingFileHandler, CompatibleSMTPSSLHandler, etc.
        :return:
        """
        # if handler_class not in (
        #     logging.StreamHandler, ColorHandler, MongoHandler, ConcurrentRotatingFileHandler, MongoHandler,
        #     CompatibleSMTPSSLHandler, ElasticHandler, DingTalkHandler, KafkaHandler):
        #     raise TypeError('Invalid handler type')
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
        # REMIND Add multi-process safe rotating file handler
        if all([self._log_path, log_filename]) and ((is_error_level_file_handler is False and self._judge_logger_has_not_handler_type(HANDLER_TYPE_FILE))
                                                    or (is_error_level_file_handler is True and self._judge_logger_has_not_handler_type(HANDLER_TYPE_ERROR_FILE))):
            if not os.path.exists(self._log_path):
                os.makedirs(self._log_path, exist_ok=True)
            log_file = str(os.path.join(self._log_path, log_filename))
            file_handler = None
            if self._log_file_handler_type == 1:
                if os_name == 'nt':
                    # ConcurrentRotatingFileHandler provides multi-process safe rotation on Windows but with significant performance cost.
                    # 10 processes each writing 100k records to the same file takes ~15 minutes - 100x slower than non-rotating writes.
                    from nb_log.handlers_concurrent_rotating_file_handler import ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos
                    file_handler = ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(log_file,
                                                                                            maxBytes=self._log_file_size * 1024 * 1024,
                                                                                            backupCount=nb_log_config_default.LOG_FILE_BACKUP_COUNT,
                                                                                            encoding="utf-8")


                elif os_name == 'posix':
                    # On Linux, ConcurrentRotatingFileHandler provides process-safe logging.
                    # 10 processes each writing 100k records takes ~100 seconds - 10x slower than non-rotating writes due to file lock overhead.
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

        # REMIND Add console handler
        if self._judge_logger_has_not_handler_type(HANDLER_TYPE_STREAM) and self._is_add_stream_handler:
            handler = ColorHandler() if not self._do_not_use_color_handler else logging.StreamHandler()
            if self._is_use_loguru_stream_handler:
                from nb_log.handlers_loguru import LoguruStreamHandler
                handler = LoguruStreamHandler(self._logger_name, sink=sys.stdout)
            # handler = logging.StreamHandler()
            handler.setLevel(self._logger_level)
            setattr(handler, MANUAL_HANLDER_TYPE, HANDLER_TYPE_STREAM)
            self.__add_a_hanlder(handler)

        self.__add_file_hanlder(self._log_filename, is_error_level_file_handler=False)
        self.__add_file_hanlder(self._error_log_filename, is_error_level_file_handler=True)

        # REMIND Add MongoDB handler.
        # if not self._judge_logger_has_handler_type(MongoHandler) and self._mongo_url:
        if self._mongo_url:
            from nb_log.handlers_more import MongoHandler
            if self._judge_logger_has_not_handler_type(MongoHandler):
                handler = MongoHandler(self._mongo_url)
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        if self._is_add_elastic_handler:
            """
            In production, cloud-based log services may be preferred over this handler.
            """
            from nb_log.handlers_more import ElasticHandler
            if self._judge_logger_has_not_handler_type(ElasticHandler):
                handler = ElasticHandler([nb_log_config_default.ELASTIC_HOST], nb_log_config_default.ELASTIC_PORT)
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        # REMIND Add Kafka handler.
        # if self._is_add_kafka_handler:
        if nb_log_config_default.RUN_ENV == 'test' and nb_log_config_default.ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT:
            from nb_log.handlers_more import KafkaHandler
            if self._judge_logger_has_not_handler_type(KafkaHandler):
                handler = KafkaHandler(nb_log_config_default.KAFKA_BOOTSTRAP_SERVERS, )
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        # REMIND Add DingTalk handler.
        if self._judge_logger_has_not_handler_type(DingTalkHandler) and self._ding_talk_token:
            handler = DingTalkHandler(self._ding_talk_token, self._ding_talk_time_interval)
            handler.setLevel(self._logger_level)
            self.__add_a_hanlder(handler)

        if self._judge_logger_has_not_handler_type(CompatibleSMTPSSLHandler) and self._is_add_mail_handler:
            handler = CompatibleSMTPSSLHandler(**self._mail_handler_config.get_dict())
            handler.setLevel(self._logger_level)
            self.__add_a_hanlder(handler)


@lru_cache()  # LogManager itself also supports unlimited instantiation
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
    Convenience function wrapping LogManager. Provides full parameter signatures for better IDE auto-completion.
    get_logger_and_add_handlers is the most commonly used method of LogManager.
    For advanced features, use the LogManager class directly.

        :param name: Logger namespace. This is the most important parameter. Different names create independent loggers with different behaviors.
                e.g. namespace 'aa' can log to console + file at INFO level, while 'bb' logs only to console at DEBUG level.
        :param log_level_int: Log output level (10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL).
       :param is_add_stream_handler: Whether to print logs to console.
       :param is_use_loguru_stream_handler: Whether to use loguru's console handler. If None, uses config default.
       :param do_not_use_color_handler: Whether to disable colored log output.
       :param log_path: Directory for log files. Defaults to nb_log_config.LOG_PATH or /pythonlogs.
       :param log_filename: Log filename. Logs are written to file only when both log_path and log_filename are not None.
       :param error_log_filename: Error log filename. If not None, ERROR+ logs are written to this separate file.
       :param log_file_size: Max log file size in MB.
       :param log_file_handler_type: File handler type (1-7). See LogManager.get_logger_and_add_handlers for details.
       :param mongo_url: MongoDB connection URL. None to skip.
       :param is_add_elastic_handler: Whether to log to Elasticsearch.
       :param is_add_kafka_handler: Whether to publish logs to Kafka.
       :param ding_talk_token: DingTalk bot token.
       :param ding_talk_time_interval: Min interval between DingTalk messages in seconds.
       :param mail_handler_config: Email handler configuration.
       :param is_add_mail_handler: Whether to send log emails.
       :param formatter_template: Log format template. Int for built-in templates, or a logging.Formatter instance.
       :type log_level_int: int
       :type is_add_stream_handler: bool
       :type log_path: str
       :type log_filename: str
       :type mongo_url: str
       :type log_file_size: int
    """
    locals_copy = copy.copy(locals())
    locals_copy.pop('name')
    # print(locals_copy)
    return LogManager(name).get_logger_and_add_handlers(**locals_copy)


@lru_cache()
def get_logger_with_filehanlder(name: str) -> logging.Logger:
    """
    Create a logger with both color console handler and file handler.
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
    Generates a logger using the class name as the namespace, allowing subclasses to use self.logger directly
    without manually instantiating get_logger.
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
    An exception that automatically logs itself when raised, eliminating the need for separate raise and log statements.
    try :
        1/0
    except Exception as e:
        raise LoggedException(message='something went wrong',)
    """

    def __init__(self, message: str, logger_obj=None, exc_info=True):
        """

        :param message:
        :param logger_obj: Provide a specific logger for logging. If provided, log_filename is not used.
        :param exc_info: Whether to include the full traceback in the log.
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
        logged_raise(ZeroDivisionError('division by zero'))

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
