

'''
误认子弟的教程
'''

from flask import Flask, request
import logging.handlers

app = Flask(__name__)

# 创建RotatingFileHandler对象并添加到app.logger.handlers列表中
file_handler = logging.handlers.RotatingFileHandler('werkzeugxx.log', maxBytes=100000, backupCount=10)
app.logger.addHandler(file_handler)

# 将Werkzeug日志级别设置为INFO
app.logger.setLevel(logging.INFO)

@app.route('/')
def hello():
    app.logger.info('Received request: %s %s %s', request.method, request.path, request.remote_addr)
    return 'Hello World!'

@app.route('/api2')
def api2():
    1/0
    return '2222'

if __name__ == '__main__':
    app.run()
