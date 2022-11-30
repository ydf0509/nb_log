
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



import  logging
import nb_log

logger = logging.getLogger('a.b.c')

logger.info('不会自动打印的')

nb_log.get_logger(None)

logger.info('这行会自动打印了，因为根命名空间加了handler')


logger1 = logging.getLogger('aaa')

logger2 = logging.getLogger('aaa')

logger3 = logging.getLogger('bbb')

print('logger1 id: ',id(logger1),'logger2 id: ',id(logger2),'logger3 id: ',id(logger3))