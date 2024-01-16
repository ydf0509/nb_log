

from loguru import logger
import requests
import logging

def errorf(x,y):
    try:
        x/y
    except Exception as e:
        logger.exception(e)


def error_req(url):
    try:
        requests.get(url)
    except Exception as e:
        # logger.exception('请求出错')
        print(logger.catch())

#errorf(2,0)
error_req('http://www.baidubgg222.com')