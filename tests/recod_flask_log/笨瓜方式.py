"""
1) 在接口中自己去手写记录请求入参和url,脱裤子放屁
2) 在接口中手写记录flask接口函数报错信息

就算你在框架层面去加日志或者接口加装饰器记录日志,来解决每个接口重复写怎么记录日志,那也是很low,

不懂日志命名空间就重复做无用功,这些记录人家框架早就帮你记录了,只是没加日志 handler,等待用户来加而已
"""
import traceback
from flask import Flask, request
from loguru import logger

app = Flask(__name__)

logger.add('mylog.log')


@app.route('/')
def hello():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr) # 写这行拖了裤子放屁
    return 'Hello World!'


@app.route('/api2')
def api2():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr)
    try:
        1 / 0  # 故意1/0 报错
        return '2222'
    except Exception as e:
        logger.error(f'e {traceback.format_exc()}')  # 写这行拖了裤子放屁


if __name__ == '__main__':
    app.run()