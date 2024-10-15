

import flask
import nb_log.global_except_hook

nb_log.get_logger(None)
app = flask.Flask(__name__)

@app.route('/')
def index():
    1/0
    return 'hello world'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)