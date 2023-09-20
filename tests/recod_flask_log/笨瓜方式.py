'''
误认子弟的教程
'''
import traceback
from flask import Flask, request
from loguru import logger

app = Flask(__name__)

logger.add('mylog.log')


@app.route('/')
def hello():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr)
    return 'Hello World!'


@app.route('/api2')
def api2():
    logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr)
    try:
        1 / 0
        return '2222'
    except Exception as e:
        logger.info(f'e {traceback.format_exc()}')


if __name__ == '__main__':
    app.run()
