"""
这个代码里面没有手写任何怎么记录flask的请求和flask异常到日志,但是可以自动记录.
这就是大神玩日志,懂命名空间.

这才是正解, werkzeug 命名空间加上各种handler,
只要请求接口,就可以记录日志到控制台和文件werkzeug.log了,

这里的flask的app的name写的是myapp ,flask框架生成的日志命名空间复用app.name,
所以给myapp加上handler,那么flask接口函数报错,就可以自动记录堆栈报错到 myapp.log 和控制台了.

"""

from flask import Flask, request
import nb_log

app = Flask('myapp')

nb_log.get_logger('werkzeug', log_filename='werkzeug.log')

nb_log.get_logger('myapp', log_filename='myapp.log')


@app.route('/')
def hello():
    # 接口中无需写日志记录请求了什么url和入参
    return 'Hello World!'


@app.route('/api2')
def api2():
    # 接口中无需写日志记录报什么错了
    1 / 0
    return '2222'


if __name__ == '__main__':
    app.run(port=5002)