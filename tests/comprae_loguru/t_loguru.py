

from loguru import logger
import urllib3

pool = urllib3.PoolManager()

logger.bind(name='urllib3',level="DEBUG")
# logger.add("urllib3_loguru.log", filter=lambda record: record["extra"].get("name") == "urllib3")

resp = pool.request('get','http://www.google.com')



logger.debug("只能打印自己的，无法记录urllib3请求了什么url")
print(resp.data)