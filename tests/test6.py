#
# #
# #
# # import flask
# # from nb_log import get_logger
# #
# #
# # # get_logger('flask',)
# # # get_logger('werkzeug')
# #
# # app = flask.Flask(__name__)
# #
# # @app.get('/')
# # def index():
# #     print('hi')
# #     return 'hi'
# #
# # app.run()
#
#
#
# # import  logging
# # import nb_log
#
# # logger = logging.getLogger('a.b.c')
# #
# # logger.info('不会自动打印的')
# #
# # nb_log.get_logger(None)
# #
# # logger.info('这行会自动打印了，因为根命名空间加了handler')
# #
# #
# # logger1 = logging.getLogger('aaa')
# #
# # logger2 = logging.getLogger('aaa')
# #
# # logger3 = logging.getLogger('bbb')
# #
# # print('logger1 id: ',id(logger1),'logger2 id: ',id(logger2),'logger3 id: ',id(logger3))
#
#
# #
# # import  logging
# # from  nb_log import get_logger
# #
# #
# # logger_foo = get_logger('foo',_log_filename='foo.log')
# #
# # logger_bar = get_logger('bar',_log_filename='bar.log')
# #
# #
# # logger_foo.debug('这句话将会写入foo.log文件')
# #
# # logger_bar.debug('这句话将会写入bar.log文件')
#
# import logging
# from nb_log.handlers import ConcurrentRotatingFileHandler,ColorHandler
# from nb_log.nb_log_config_default import FORMATTER_DICT
#
# logger = logging.getLogger('foo')
#
# logger.setLevel(logging.DEBUG)
#
# ch = ColorHandler()
# ch.setLevel(logging.INFO)
# ch.setFormatter(FORMATTER_DICT[7])
# logger.addHandler(ch)
#
# fh = ConcurrentRotatingFileHandler('foo.log')
# fh.setLevel(logging.ERROR)
# fh.setFormatter(FORMATTER_DICT[11])
# logger.addHandler(fh)
#
#
# logger.debug('debug debug')
# logger.info('info info')
# logger.warning('warning warning')
# logger.error('error error ')
# logger.critical('critical critical')
#


# import logging
#
# logger = logging.getLogger('abc')
#
# print(__name__)
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(10)
# logger.debug('hah')

import requests
import nb_log

# nb_log.get_logger('urllib3',log_level_int=10) # log_level_int=10 或者 logging.DEBUG
#
# requests.get('https://ww.baidu.com')


import logging
import nb_log

#
# nb_log.LogManager('name1').preset_log_level(20)
#
# logger = nb_log.get_logger('name1',log_level_int=10)
# # logger.setLevel(10)
# logger.debug('啊啊啊')
#
#
# import celery
#
# import flask
#
# import fastapi
# nb_log.get_logger('')
# logging.getLogger('b6').debug(666)
#
# print(logging.Manager(logging.root).loggerDict)

from nb_log import get_logger

from nb_log import get_logger


class 废物日志类:
    def __init__(self,name):
        self.logger = get_logger(name, log_filename='废物日志.log')

    def debug(self, msg):
        self.logger.debug(msg, extra={'sys_getframe_n': 3})  # 第 x1 行

    def info(self, msg):
        self.logger.info(msg, extra={'sys_getframe_n': 3})  # 第 x2 行

    def critical(self, msg):
        self.logger.critical(msg, extra={'sys_getframe_n': 3},exc_info=True)  # 第 x2 行

try:
    1/0
except Exception as e:
    废物日志类('命名空间1').critical('啊啊啊啊')  # 第y行