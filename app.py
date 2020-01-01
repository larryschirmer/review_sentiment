import os
from flask import Flask, request
from gevent.pywsgi import WSGIServer

project_filename = "_sentiment_doc_2_vec"
env = os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')

app = Flask(__name__)
app.config.from_object(env)


@app.route('/', methods=['GET'])
def hello():
    return {
        'data': 'hi, POST a review in a body with key \'review\''
    }


@app.route('/', methods=['POST'])
def hello_name():
    review = request.json['review']
    return review


if __name__ == '__main__':
    if env == 'config.ProductionConfig':
        # Production
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    else:
        # Debug/Development
        app.run(port="5000")
