# coding=utf8
# noinspection SpellCheckingInspection
"""
日志管理，支持日志打印到控制台和写入切片文件和mongodb和email和钉钉机器人和elastic和kafka。
建造者模式一键创建返回添加了各种好用的handler的原生官方Logger对象，兼容性扩展性极强。
使用观察者模式按照里面的例子可以扩展各种有趣的handler。
使用方式为  logger = LogManager('logger_name').get_and_add_handlers(log_level_int=1, is_add_stream_handler=True,
 log_path=None, log_filename=None, log_file_size=10,mongo_url=None,formatter_template=2)


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
import typing
from functools import lru_cache
from logging import FileHandler, _checkLevel  # noqa
from nb_log import nb_log_config_default, compatible_logger  # noqa
from nb_log.compatible_logger import CompatibleLogger
from nb_log.handlers import *
import deprecated

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


# noinspection PyProtectedMember
def revision_add_handler(self, hdlr):  # 从添加源头阻止同一个logger添加同类型的handler。
    """
    Add the specified handler to this logger.
    """
    logging._acquireLock()  # noqa

    try:
        """ 官方的
        if not (hdlr in self.handlers):
            self.handlers.append(hdlr)
        """
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
    finally:
        logging._releaseLock()  # noqa


def revision_setLevel(self, level):
    """
    Set the logging level of this logger.  level must be an int or a str.
    """
    level2 = LogManager.preset_name__level_map.get(self.name, level)
    if level2 != level:
        very_nb_print(f'日志命名空间 {self.name} 已经锁定了为了 {level2} 级别 ,后续不可以更改为 {level} 级别')
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


LOG_LEVEL_LIST = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]  # 就是 10 20 30 40 50


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

    @staticmethod
    def get_all_logging_name():
        return get_all_logging_name()

    def __init__(self, logger_name: typing.Union[str, None] = 'nb_log_default_namespace', logger_cls=logging.Logger):
        """
        :param logger_name: 日志名称，当为None时候创建root命名空间的日志，一般情况下千万不要传None，除非你确定需要这么做和是在做什么.这个命名空间是双刃剑
        """
        if logger_name in (None, '',) and multiprocessing.process.current_process().name == 'MainProcess':
            very_nb_print('logger_name 设置为None和空字符串都是一个意义，在操作根日志命名空间，任何其他日志的行为将会发生变化，'
                          '一定要弄清楚原生logging包的日志name的意思。这个命名空间是双刃剑')
        self._logger_name = logger_name
        if logger_cls == logging.Logger:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logger_cls(logger_name)

    @staticmethod
    def generate_error_file_name(log_filename: str):
        if log_filename is None:
            return None
        arr = log_filename.split('.')
        part1 = '.'.join(arr[:-1])
        part2 = arr[-1]
        return f'{part1}_error.{part2}'

    def preset_log_level(self, log_level_int=20):
        """
        提前设置锁定日志级别，当之后再设置该命名空间日志的级别的时候，按照提前预设的级别，无视之后设定的级别。
        主要是针对动态初始化的日志，在生成日志之后再去设置日志级别不方便。
        :param log_level_int:logging.DEBUG LOGGING.INFO 等
        :return:
        """
        check_log_level(log_level_int)
        self.preset_name__level_map[self._logger_name] = log_level_int

    # 加*是为了强制在调用此方法时候使用关键字传参，如果以位置传参强制报错，因为此方法后面的参数中间可能以后随时会增加更多参数，造成之前的使用位置传参的代码参数意义不匹配。
    # noinspection PyAttributeOutsideInit
    def get_logger_and_add_handlers(self, log_level_int: int = None, *, is_add_stream_handler=True,
                                    is_use_loguru_stream_handler:bool=None,
                                    do_not_use_color_handler=None, log_path=None,
                                    log_filename=None, log_file_size: int = None,
                                    log_file_handler_type: int = None,
                                    error_log_filename=None,
                                    mongo_url=None, is_add_elastic_handler=False, is_add_kafka_handler=False,
                                    ding_talk_token=None, ding_talk_time_interval=60,
                                    mail_handler_config: MailHandlerConfig = MailHandlerConfig(),
                                    is_add_mail_handler=False,
                                    formatter_template: typing.Union[int, logging.Formatter] = None):
        """
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
            error_log_filename = self.generate_error_file_name(log_filename)
        self._error_log_filename = error_log_filename
        self._log_file_size = log_file_size
        if log_file_handler_type not in (None, 1, 2, 3, 4, 5, 6,7):
            raise ValueError("log_file_handler_type的值必须设置为 1 2 3 4 5 6 7这几个数字")
        self._log_file_handler_type = log_file_handler_type or nb_log_config_default.LOG_FILE_HANDLER_TYPE
        self._mongo_url = mongo_url
        self._is_add_elastic_handler = is_add_elastic_handler
        self._is_add_kafka_handler = is_add_kafka_handler
        self._ding_talk_token = ding_talk_token
        self._ding_talk_time_interval = ding_talk_time_interval
        self._mail_handler_config = mail_handler_config
        self._is_add_mail_handler = is_add_mail_handler
        self._is_use_loguru_stream_handler = nb_log_config_default.DEFAULUT_IS_USE_LOGURU_STREAM_HANDLER  if is_use_loguru_stream_handler is None\
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

    def remove_handler_by_handler_class(self, handler_class: typing.Union[type,str]):
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
        handlerx.setLevel(10)
        handlerx.setFormatter(self._formatter)
        self.logger.addHandler(handlerx)

    # def _judge_logger_has_handler_type(self, handler_type: typing.Union[type,str]):
    #     for hr in self.logger.handlers:
    #         if isinstance(hr, handler_type):
    #             return True

    def _judge_logger_has_not_handler_type(self, handler_type: typing.Union[type,str]):
        for hr in self.logger.handlers:
            if _get_hanlder_type(hr)==handler_type:
                return False
        return True

    def __add_file_hanlder(self, log_filename, is_error_level_file_handler):
        # REMIND 添加多进程安全切片的文件日志
        if all([self._log_path, log_filename]) and ((is_error_level_file_handler is False and self._judge_logger_has_not_handler_type(HANDLER_TYPE_FILE))
            or (is_error_level_file_handler is True and self._judge_logger_has_not_handler_type(HANDLER_TYPE_ERROR_FILE)) ):
            if not os.path.exists(self._log_path):
                os.makedirs(self._log_path, exist_ok=True)
            log_file = os.path.join(self._log_path, log_filename)
            file_handler = None
            if self._log_file_handler_type == 1:
                if os_name == 'nt':
                    # 在win下使用这个ConcurrentRotatingFileHandler可以解决多进程安全切片，但性能损失惨重。
                    # 10进程各自写入10万条记录到同一个文件消耗15分钟。比不切片写入速度降低100倍。
                    file_handler = ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(log_file,
                                                                                            maxBytes=self._log_file_size * 1024 * 1024,
                                                                                            backupCount=nb_log_config_default.LOG_FILE_BACKUP_COUNT,
                                                                                            encoding="utf-8")


                elif os_name == 'posix':
                    # linux下可以使用ConcurrentRotatingFileHandler，进程安全的日志方式。
                    # 10进程各自写入10万条记录到同一个文件消耗100秒，还是比不切片写入速度降低10倍。因为每次检查切片大小和文件锁的原因。
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
                file_handler = LoguruFileHandler(logger_name=self._logger_name,sink=log_file)

            if is_error_level_file_handler:
                setattr(file_handler, MANUAL_HANLDER_TYPE, HANDLER_TYPE_ERROR_FILE)
                file_handler.setLevel(logging.ERROR)
            else:
                setattr(file_handler, MANUAL_HANLDER_TYPE, HANDLER_TYPE_FILE)
                file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(self._formatter)
            self.logger.addHandler(file_handler)

    def __add_handlers(self):
        pass

        # REMIND 添加控制台日志
        if self._judge_logger_has_not_handler_type(HANDLER_TYPE_STREAM) and self._is_add_stream_handler:
            handler = ColorHandler() if not self._do_not_use_color_handler else logging.StreamHandler()  # 不使用streamhandler，使用自定义的彩色日志
            if self._is_use_loguru_stream_handler:
                from nb_log.handlers_loguru import LoguruStreamHandler
                handler = LoguruStreamHandler(self._logger_name,sink=sys.stdout)
            # handler = logging.StreamHandler()
            handler.setLevel(self._logger_level)
            setattr(handler,MANUAL_HANLDER_TYPE,HANDLER_TYPE_STREAM)
            self.__add_a_hanlder(handler)

        self.__add_file_hanlder(self._log_filename, is_error_level_file_handler=False)
        self.__add_file_hanlder(self._error_log_filename, is_error_level_file_handler=True)

        # REMIND 添加mongo日志。
        # if not self._judge_logger_has_handler_type(MongoHandler) and self._mongo_url:
        if self._mongo_url :
            from nb_log.handlers_more import MongoHandler
            if  self._judge_logger_has_not_handler_type(MongoHandler):
                handler = MongoHandler(self._mongo_url)
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        if self._is_add_elastic_handler:
            """
            生产环境使用阿里云 oss日志，不使用这个。
            """
            from nb_log.handlers_more import ElasticHandler
            if  self._judge_logger_has_not_handler_type(ElasticHandler):
                handler = ElasticHandler([nb_log_config_default.ELASTIC_HOST], nb_log_config_default.ELASTIC_PORT)
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        # REMIND 添加kafka日志。
        # if self._is_add_kafka_handler:
        if nb_log_config_default.RUN_ENV == 'test' and nb_log_config_default.ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT:
            from nb_log.handlers_more import KafkaHandler
            if  self._judge_logger_has_not_handler_type(KafkaHandler):
                handler = KafkaHandler(nb_log_config_default.KAFKA_BOOTSTRAP_SERVERS, )
                handler.setLevel(self._logger_level)
                self.__add_a_hanlder(handler)

        # REMIND 添加钉钉日志。
        if  self._judge_logger_has_not_handler_type(DingTalkHandler) and self._ding_talk_token:
            handler = DingTalkHandler(self._ding_talk_token, self._ding_talk_time_interval)
            handler.setLevel(self._logger_level)
            self.__add_a_hanlder(handler)

        if  self._judge_logger_has_not_handler_type(CompatibleSMTPSSLHandler) and self._is_add_mail_handler:
            handler = CompatibleSMTPSSLHandler(**self._mail_handler_config.get_dict())
            handler.setLevel(self._logger_level)
            self.__add_a_hanlder(handler)


@lru_cache()  # LogManager 本身也支持无限实例化
def get_logger(name: typing.Union[str, None], *, log_level_int: int = None, is_add_stream_handler=True,
               is_use_loguru_stream_handler:bool=None,
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
