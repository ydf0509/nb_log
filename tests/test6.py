from nb_log import get_logger
import requests

get_logger('urllib3')
requests.get("http://www.baidu.com")

