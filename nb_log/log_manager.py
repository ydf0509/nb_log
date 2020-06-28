# coding=utf8
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
import unittest
from functools import lru_cache

from nb_log.handlers import *
from nb_log import nb_log_config_default


def revision_call_handlers(self, record):  # 对logging标准模块打猴子补丁。主要是使父命名空间的handler不重复记录当前命名空间日志已有种类的handler。
    """
    重要。这可以使同名logger或父logger随意添加同种类型的handler，确保不会重复打印。

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
            hdlr_type = type(hdlr)
            if hdlr_type == logging.StreamHandler:  # REMIND 因为很多handler都是继承自StreamHandler，包括filehandler，直接判断会逻辑出错。
                hdlr_type = ColorHandler
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
            self.manager.emittedNoHandlerWarning = True


# noinspection PyProtectedMember
def revision_add_handler(self, hdlr):  # 从添加源头阻止同一个logger添加同类型的handler。
    """
    Add the specified handler to this logger.
    """
    logging._acquireLock()

    try:
        """ 官方的
        if not (hdlr in self.handlers):
            self.handlers.append(hdlr)
        """
        hdlrx_type_set = set()
        for hdlrx in self.handlers:
            hdlrx_type = type(hdlrx)
            if hdlrx_type == logging.StreamHandler:  # REMIND 因为很多handler都是继承自StreamHandler，包括filehandler，直接判断会逻辑出错。
                hdlrx_type = ColorHandler
            hdlrx_type_set.add(hdlrx_type)

        hdlr_type = type(hdlr)
        if hdlr_type == logging.StreamHandler:
            hdlr_type = ColorHandler
        if hdlr_type not in hdlrx_type_set:
            self.handlers.append(hdlr)
    finally:
        logging._releaseLock()


logging.Logger.callHandlers = revision_call_handlers  # 打猴子补丁。
logging.Logger.addHandler = revision_add_handler  # 打猴子补丁。


# noinspection PyShadowingBuiltins
# print = very_nb_print


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


# noinspection PyMissingOrEmptyDocstring,PyPep8
class LogManager(object):
    """
    一个日志管理类，用于创建logger和添加handler，支持将日志打印到控制台打印和写入日志文件和mongodb和邮件。
    """
    logger_name_list = []
    logger_list = []

    def __init__(self, logger_name='nb_log_default_namespace'):
        """
        :param logger_name: 日志名称，当为None时候创建root命名空间的日志，一般情况下千万不要传None，除非你确定需要这么做和是在做什么.这个命名空间是双刃剑
        """
        if logger_name in (None, '', 'root'):
            very_nb_print('logger_name 设置为None和root和空字符串都是一个意义，在操作根日志命名空间，任何其他日志的行为将会发生变化，一定要弄清楚原生logging包的日志name的意思。这个命名空间是双刃剑')
        self._logger_name = logger_name
        self.logger = logging.getLogger(logger_name)

    # 加*是为了强制在调用此方法时候使用关键字传参，如果以位置传参强制报错，因为此方法后面的参数中间可能以后随时会增加更多参数，造成之前的使用位置传参的代码参数意义不匹配。
    # noinspection PyAttributeOutsideInit
    def get_logger_and_add_handlers(self, log_level_int: int = None, *, is_add_stream_handler=True,
                                    do_not_use_color_handler=None, log_path='/pythonlogs',
                                    log_filename=None, log_file_size: int = None,
                                    mongo_url=None, is_add_elastic_handler=False, is_add_kafka_handler=False,
                                    ding_talk_token=None, ding_talk_time_interval=60,
                                    mail_handler_config: MailHandlerConfig = MailHandlerConfig(), is_add_mail_handler=False,
                                    formatter_template: int = None):
        """
       :param log_level_int: 日志输出级别，设置为 1 2 3 4 5，分别对应原生logging.DEBUG(10)，logging.INFO(20)，logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，现在可以直接用10 20 30 40 50了，兼容了。
       :param is_add_stream_handler: 是否打印日志到控制台
       :param do_not_use_color_handler :是否禁止使用color彩色日志
       :param log_path: 设置存放日志的文件夹路径
       :param log_filename: 日志的名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
       :param log_file_size :日志大小，单位M，默认100M
       :param mongo_url : mongodb的连接，为None时候不添加mongohandler
       :param is_add_elastic_handler: 是否记录到es中。
       :param is_add_kafka_handler: 日志是否发布到kafka。
       :param ding_talk_token:钉钉机器人token
       :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
       :param mail_handler_config : 邮件配置
       :param is_add_mail_handler :是否发邮件
       :param formatter_template :日志模板，1为formatter_dict的详细模板，2为简要模板,5为最好模板
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
        if formatter_template is None:
            formatter_template = nb_log_config_default.FORMATTER_KIND

        self._logger_level = log_level_int * 10 if log_level_int < 10 else log_level_int
        self._is_add_stream_handler = is_add_stream_handler
        self._do_not_use_color_handler = do_not_use_color_handler
        self._log_path = log_path
        self._log_filename = log_filename
        self._log_file_size = log_file_size
        self._mongo_url = mongo_url
        self._is_add_elastic_handler = is_add_elastic_handler
        self._is_add_kafka_handler = is_add_kafka_handler
        self._ding_talk_token = ding_talk_token
        self._ding_talk_time_interval = ding_talk_time_interval
        self._mail_handler_config = mail_handler_config
        self._is_add_mail_handler = is_add_mail_handler

        self._formatter = nb_log_config_default.FORMATTER_DICT[formatter_template]

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
        for hd in self.logger.handlers:
            self.logger.removeHandler(hd)

    def remove_handler_by_handler_class(self, handler_class: type):
        """
        去掉指定类型的handler
        :param handler_class:logging.StreamHandler,ColorHandler,MongoHandler,ConcurrentRotatingFileHandler,MongoHandler,CompatibleSMTPSSLHandler的一种
        :return:
        """
        if handler_class not in (
                logging.StreamHandler, ColorHandler, MongoHandler, ConcurrentRotatingFileHandler, MongoHandler,
                CompatibleSMTPSSLHandler, ElasticHandler, DingTalkHandler, KafkaHandler):
            raise TypeError('设置的handler类型不正确')
        for handler in self.logger.handlers:
            if isinstance(handler, handler_class):
                self.logger.removeHandler(handler)  # noqa

    def __add_a_hanlder(self, handlerx: logging.Handler):
        handlerx.setLevel(10)
        handlerx.setFormatter(self._formatter)
        self.logger.addHandler(handlerx)

    def _judge_logger_has_handler_type(self, handler_type: type):
        for hr in self.logger.handlers:
            if isinstance(hr, handler_type):
                return True

    def __add_handlers(self):
        pass

        # REMIND 添加控制台日志
        if not (self._judge_logger_has_handler_type(ColorHandler) or self._judge_logger_has_handler_type(
                logging.StreamHandler)) and self._is_add_stream_handler:
            handler = ColorHandler() if not self._do_not_use_color_handler else logging.StreamHandler()  # 不使用streamhandler，使用自定义的彩色日志
            # handler = logging.StreamHandler()
            self.__add_a_hanlder(handler)

        # REMIND 添加多进程安全切片的文件日志
        if not self._judge_logger_has_handler_type(ConcurrentRotatingFileHandler) and all(
                [self._log_path, self._log_filename]):
            if not os.path.exists(self._log_path):
                os.makedirs(self._log_path)
            log_file = os.path.join(self._log_path, self._log_filename)
            rotate_file_handler = None
            if os_name == 'nt':
                # 在win下使用这个ConcurrentRotatingFileHandler可以解决多进程安全切片，但性能损失惨重。
                # 10进程各自写入10万条记录到同一个文件消耗15分钟。比不切片写入速度降低100倍。
                rotate_file_handler = ConcurrentRotatingFileHandlerWithBufferInitiativeWindwos(log_file,
                                                                                               maxBytes=self._log_file_size * 1024 * 1024,
                                                                                               backupCount=nb_log_config_default.LOG_FILE_BACKUP_COUNT,
                                                                                               encoding="utf-8")
            elif os_name == 'posix':
                # linux下可以使用ConcurrentRotatingFileHandler，进程安全的日志方式。
                # 10进程各自写入10万条记录到同一个文件消耗100秒，还是比不切片写入速度降低10倍。因为每次检查切片大小和文件锁的原因。
                rotate_file_handler = ConcurrentRotatingFileHandlerWithBufferInitiativeLinux(log_file,
                                                                                             maxBytes=self._log_file_size * 1024 * 1024,
                                                                                             backupCount=nb_log_config_default.LOG_FILE_BACKUP_COUNT,
                                                                                             encoding="utf-8")
            self.__add_a_hanlder(rotate_file_handler)

        # REMIND 添加mongo日志。
        if not self._judge_logger_has_handler_type(MongoHandler) and self._mongo_url:
            self.__add_a_hanlder(MongoHandler(self._mongo_url))

        if not self._judge_logger_has_handler_type(
                ElasticHandler) and self._is_add_elastic_handler and nb_log_config_default.RUN_ENV == 'test':  # 使用kafka。不直接es。
            """
            生产环境使用阿里云 oss日志，不使用这个。
            """
            self.__add_a_hanlder(
                ElasticHandler([nb_log_config_default.ELASTIC_HOST], nb_log_config_default.ELASTIC_PORT))

        # REMIND 添加kafka日志。
        # if self._is_add_kafka_handler:
        if not self._judge_logger_has_handler_type(
                KafkaHandler) and nb_log_config_default.RUN_ENV == 'test' \
                and nb_log_config_default.ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT:
            self.__add_a_hanlder(KafkaHandler(nb_log_config_default.KAFKA_BOOTSTRAP_SERVERS, ))

        # REMIND 添加钉钉日志。
        if not self._judge_logger_has_handler_type(DingTalkHandler) and self._ding_talk_token:
            self.__add_a_hanlder(DingTalkHandler(self._ding_talk_token, self._ding_talk_time_interval))

        if not self._judge_logger_has_handler_type(CompatibleSMTPSSLHandler) and self._is_add_mail_handler:
            self.__add_a_hanlder(CompatibleSMTPSSLHandler(**self._mail_handler_config.get_dict()))


@lru_cache()
def get_logger(name: str, *, log_level_int: int = None, is_add_stream_handler=True,
               do_not_use_color_handler=None, log_path='/pythonlogs',
               log_filename=None, log_file_size: int = None,
               mongo_url=None, is_add_elastic_handler=False, is_add_kafka_handler=False,
               ding_talk_token=None, ding_talk_time_interval=60,
               mail_handler_config: MailHandlerConfig = MailHandlerConfig(), is_add_mail_handler=False,
               formatter_template: int = None) -> logging.Logger:
    """
    重写一遍，是为了更好的pycharm自动补全，所以不用**kwargs的写法。
    如果太喜欢函数调用了，可以使用这种
       :param name: 日志命名空间，重要。
       :param log_level_int: 日志输出级别，设置为 1 2 3 4 5，分别对应原生logging.DEBUG(10)，logging.INFO(20)，
       logging.WARNING(30)，logging.ERROR(40),logging.CRITICAL(50)级别，现在可以直接用10 20 30 40 50了，兼容了。

       :param is_add_stream_handler: 是否打印日志到控制台
       :param do_not_use_color_handler :是否禁止使用color彩色日志
       :param log_path: 设置存放日志的文件夹路径
       :param log_filename: 日志的名字，仅当log_path和log_filename都不为None时候才写入到日志文件。
       :param log_file_size :日志大小，单位M，默认100M
       :param mongo_url : mongodb的连接，为None时候不添加mongohandler
       :param is_add_elastic_handler: 是否记录到es中。
       :param is_add_kafka_handler: 日志是否发布到kafka。
       :param ding_talk_token:钉钉机器人token
       :param ding_talk_time_interval : 时间间隔，少于这个时间不发送钉钉消息
       :param mail_handler_config : 邮件配置
       :param is_add_mail_handler :是否发邮件
       :param formatter_template :日志模板，1为formatter_dict的详细模板，2为简要模板,5为最好模板
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


class LoggerMixin(object):
    subclass_logger_dict = {}

    @property
    def logger_extra_suffix(self):
        return self.__logger_extra_suffix

    @logger_extra_suffix.setter
    def logger_extra_suffix(self, value):
        # noinspection PyAttributeOutsideInit
        self.__logger_extra_suffix = value

    @property
    def logger_full_name(self):
        try:
            # noinspection PyUnresolvedReferences
            return type(self).__name__ + '-' + self.logger_extra_suffix
        except AttributeError:
            # very_nb_print(type(e))
            return type(self).__name__

    @property
    def logger(self):
        logger_name_key = self.logger_full_name + '1'
        if logger_name_key not in self.subclass_logger_dict:
            logger_var = LogManager(self.logger_full_name).get_logger_and_add_handlers()
            self.subclass_logger_dict[logger_name_key] = logger_var
            return logger_var
        else:
            return self.subclass_logger_dict[logger_name_key]

    @property
    def logger_with_file(self):
        logger_name_key = self.logger_full_name + '2'
        if logger_name_key not in self.subclass_logger_dict:
            logger_var = LogManager(self.logger_full_name).get_logger_and_add_handlers(
                log_filename=self.logger_full_name + '.log', log_file_size=50)
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
                log_filename=self.logger_full_name + '.log', log_file_size=50)
            self.subclass_logger_dict[logger_name_key] = logger_var
            return logger_var
        else:
            return self.subclass_logger_dict[logger_name_key]


class LoggerLevelSetterMixin:
    # noinspection PyUnresolvedReferences
    def set_log_level(self, log_level=10):
        try:
            self.logger.setLevel(log_level)
        except AttributeError as e:
            very_nb_print(e)

        return self


# noinspection PyMethodMayBeStatic,PyNestedDecorators,PyArgumentEqualDefault
class _Test(unittest.TestCase):
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def tearDownClass(cls):
        """

        """
        time.sleep(1)

    @unittest.skip
    def test_repeat_add_handlers_(self):
        """测试重复添加handlers"""
        LogManager('tests').get_logger_and_add_handlers(log_path='../logs', log_filename='tests.log')
        LogManager('tests').get_logger_and_add_handlers(log_path='../logs', log_filename='tests.log')
        LogManager('tests').get_logger_and_add_handlers(log_path='../logs', log_filename='tests.log')
        test_log = LogManager('tests').get_logger_and_add_handlers(log_path='../logs', log_filename='tests.log')
        print('下面这一句不会重复打印四次和写入日志四次')
        time.sleep(1)
        test_log.debug('这一句不会重复打印四次和写入日志四次')

    @unittest.skip
    def test_get_logger_without_hanlders(self):
        """测试没有handlers的日志"""
        log = LogManager('test2').get_logger_without_handlers()
        print('下面这一句不会被打印')
        time.sleep(1)
        log.info('这一句不会被打印')

    @unittest.skip
    def test_add_handlers(self):
        """这样可以在具体的地方任意写debug和info级别日志，只需要在总闸处规定级别就能过滤，很方便"""
        LogManager('test3').get_logger_and_add_handlers(2)
        log1 = LogManager('test3').get_logger_without_handlers()
        print('下面这一句是info级别，可以被打印出来')
        time.sleep(1)
        log1.info('这一句是info级别，可以被打印出来')
        print('下面这一句是debug级别，不能被打印出来')
        time.sleep(1)
        log1.debug('这一句是debug级别，不能被打印出来')

    @unittest.skip
    def test_only_write_log_to_file(self):  # NOQA
        """只写入日志文件"""
        log5 = LogManager('test5').get_logger_and_add_handlers(20)
        log6 = LogManager('test6').get_logger_and_add_handlers(is_add_stream_handler=False, log_filename='test6.log')
        print('下面这句话只写入文件')
        log5.debug('这句话只写入文件')
        log6.debug('这句话只写入文件')

    @unittest.skip
    def test_none(self):
        # noinspection PyUnusedLocal
        log1 = LogManager('log1').get_logger_and_add_handlers()
        LogManager().get_logger_and_add_handlers()

        LogManager().get_logger_and_add_handlers()
        log1 = LogManager('log1').get_logger_and_add_handlers()
        LogManager().get_logger_and_add_handlers()
        LogManager('log1').get_logger_and_add_handlers(log_filename='test_none.log')
        log1.debug('打印几次？')

    @unittest.skip
    def test_formater(self):
        logger2 = LogManager('test_formater2').get_logger_and_add_handlers(formatter_template=6)
        logger2.debug('测试日志模板2')
        logger5 = LogManager('test_formater5').get_logger_and_add_handlers(formatter_template=5)
        logger5.error('测试日志模板5')

    @unittest.skip
    def test_ding_talk(self):
        logger = LogManager('testdinding').get_logger_and_add_handlers(
            ding_talk_token=nb_log_config_default.DING_TALK_TOKEN,
            ding_talk_time_interval=10)
        logger.debug('啦啦啦德玛西亚1')
        logger.debug('啦啦啦德玛西亚2')
        time.sleep(10)
        logger.debug('啦啦啦德玛西亚3')

    @unittest.skip
    def test_remove_handler(self):
        logger = LogManager('test13').get_logger_and_add_handlers()
        logger.debug('去掉coloerhandler前')
        LogManager('test13').remove_handler_by_handler_class(ColorHandler)
        logger.debug('去掉coloerhandler后，此记录不会被打印')

    @unittest.skip
    def test_logging(self):
        # logging命名空间是root,会导致日志重复打印，不要直接用。
        logger = LogManager('test14').get_logger_and_add_handlers(formatter_template=4)
        logger.debug('xxxx')
        logging.warning('yyyyyyy')
        logger.warning('zzzzzzzzz')

    @unittest.skip
    def test_logger_level_setter_mixin(self):
        """
        测试可以设置日志级别的mixin类
        :return:
        """
        print('测试非常流弊的print')

        class A(LoggerMixin, LoggerLevelSetterMixin):
            pass

        a = A().set_log_level(20)
        a.logger.debug('这句话不能被显示')  # 这句话不能被打印
        a.logger.error('这句话可以显示')

    # @unittest.skip
    def test_color_and_mongo_hanlder(self):
        """测试彩色日志和日志写入mongodb"""
        very_nb_print('测试颜色和mongo')

        # logger = LogManager('helloMongo', is_pycharm_2019=False).get_logger_and_add_handlers(mongo_url=app_config.connect_url, formatter_template=5)
        logging.error('xxxx')
        logger = LogManager('helloMongo').get_logger_and_add_handlers(formatter_template=5, is_add_elastic_handler=True)
        logger.addHandler(ColorHandler())  # 由于打了强大的猴子补丁，无惧反复添加同种handler。
        logger.addHandler(ColorHandler())
        logger.addHandler(ColorHandler())
        for i in range(1000000):
            time.sleep(0.1)
            logger.debug('一个debug级别的日志。' * 3)
            logger.info('一个info级别的日志。' * 3)
            logger.warning('一个warning级别的日志。' * 3)
            logger.error('一个error级别的日志。' * 3)
            logger.critical('一个critical级别的日志。' * 3)

    @unittest.skip
    def test_all_handlers(self):
        logger = LogManager('hi').get_logger_and_add_handlers(log_filename='hi.log',
                                                              ding_talk_token=nb_log_config_default.DING_TALK_TOKEN,
                                                              mongo_url=nb_log_config_default.MONGO_URL,
                                                              formatter_template=5)
        logger.debug('测试多种handler')


def test_multiprocess_file_handler():
    t1 = time.time()
    logger = LogManager('abcd').get_logger_and_add_handlers(is_add_stream_handler=False,
                                                            log_filename='amulti_test99.log', log_file_size=200)
    for i in range(1000000, 2000000):
        # time.sleep(0.000001)
        logger.debug(f'{i}a')
        if i % 10000 == 0:
            very_nb_print(i)
    very_nb_print(time.time() - t1)
    time.sleep(10)


if __name__ == "__main__":
    unittest.main()
    # from multiprocessing import Process
    #
    # [Process(target=test_multiprocess_file_handler).start() for _ in range(10)]
