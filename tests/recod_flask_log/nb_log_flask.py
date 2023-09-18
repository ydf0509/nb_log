


'''
误认子弟的教程
'''

from flask import Flask, request
import nb_log

app = Flask('importnamexx')

nb_log.get_logger('werkzeug',log_filename='werkzeug.log')

nb_log.get_logger('importnamexx',log_filename='importnamexx.log')

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/api2')
def api2():
    1/0
    return '2222'

if __name__ == '__main__':
    app.run(port=5002)