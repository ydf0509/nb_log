import requests
from nb_log import get_logger
import pymysql

logger = get_logger('urllib3', log_filename='urllib3.log', )

logger2 = get_logger('pymysql', log_filename='pymysql.log', )
requests.get('http://www.baidu.com')


conn = pymysql.Connection(user='root',password='123456')
cur = conn.cursor()

cur.execute('select "abc" as x')
print(cur.fetchall())
# logger.debug(11, extra={'c': 5, 'd': 6})
# logger.info(22)
# logger.warning(33)
# logger.error(44)
# logger.critical(55,extra=dict(f=7,g=8,h=9))
#
# logger.debug('哈哈哈哈', extra=dict(a=1, b=2))
# try:
#     1 / 0
# except Exception as e:
#     logger.exception('错误了')
