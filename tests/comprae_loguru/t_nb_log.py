import requests

import nb_log
import urllib3

logger = nb_log.get_logger('urllib3')

pool = urllib3.PoolManager()
resp = pool.request('get','http://www.google.com')

logger.debug("除了能打印这行，还能自动记录urllib3请求了什么url")

print(resp.data)