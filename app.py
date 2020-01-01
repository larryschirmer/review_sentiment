import os
from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"


@app.route('/<name>', methods=['GET'])
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    if os.environ['APP_SETTINGS'] == 'config.ProductionConfig':
        # Production
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    else:
        # Debug/Development
        app.run(port="5000")
