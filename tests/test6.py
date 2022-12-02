
#
#
# import flask
# from nb_log import get_logger
#
#
# # get_logger('flask',)
# # get_logger('werkzeug')
#
# app = flask.Flask(__name__)
#
# @app.get('/')
# def index():
#     print('hi')
#     return 'hi'
#
# app.run()



# import  logging
# import nb_log

# logger = logging.getLogger('a.b.c')
#
# logger.info('不会自动打印的')
#
# nb_log.get_logger(None)
#
# logger.info('这行会自动打印了，因为根命名空间加了handler')
#
#
# logger1 = logging.getLogger('aaa')
#
# logger2 = logging.getLogger('aaa')
#
# logger3 = logging.getLogger('bbb')
#
# print('logger1 id: ',id(logger1),'logger2 id: ',id(logger2),'logger3 id: ',id(logger3))


#
# import  logging
# from  nb_log import get_logger
#
#
# logger_foo = get_logger('foo',log_filename='foo.log')
#
# logger_bar = get_logger('bar',log_filename='bar.log')
#
#
# logger_foo.debug('这句话将会写入foo.log文件')
#
# logger_bar.debug('这句话将会写入bar.log文件')

import logging
from nb_log.handlers import ConcurrentRotatingFileHandler,ColorHandler
from nb_log.nb_log_config_default import FORMATTER_DICT

logger = logging.getLogger('foo')

logger.setLevel(logging.DEBUG)

ch = ColorHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(FORMATTER_DICT[7])
logger.addHandler(ch)

fh = ConcurrentRotatingFileHandler('foo.log')
fh.setLevel(logging.ERROR)
fh.setFormatter(FORMATTER_DICT[11])
logger.addHandler(fh)


logger.debug('debug debug')
logger.info('info info')
logger.warning('warning warning')
logger.error('error error ')
logger.critical('critical critical')

