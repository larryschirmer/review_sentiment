import os
from flask import Flask
from gevent.pywsgi import WSGIServer

project_filename = "_sentiment_doc_2_vec"
env = os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')

app = Flask(__name__)
app.config.from_object(env)


@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"


@app.route('/<name>', methods=['GET'])
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    if env == 'config.ProductionConfig':
        # Production
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    else:
        # Debug/Development
        app.run(port="5000")
