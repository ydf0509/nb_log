from nb_log import get_logger,LogManager
import requests

get_logger('urllib3')
requests.get("http://www.baidu.com")


LogManager('abcd').preset_log_level(20)
l1 = get_logger('abcd',log_level_int=20)
l2 = get_logger('abcd',log_level_int=30)


l1.debug('能显示不？')

l1.info('能显示不？')