import os
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from keras.models import load_model

from utils import get_review_sentiment, get_vocab

project_filename = "_sentiment_doc_2_vec"
env = os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
model = load_model(project_filename + '_model.h5')
vocab = get_vocab(project_filename + '_vocab.txt')

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
    review_sentiment, review_confidence = get_review_sentiment(
        review, model, vocab)
    return {
        "sentiment": review_sentiment,
        "confidence": review_confidence
    }


if __name__ == '__main__':
    if env == 'config.ProductionConfig':
        # Production
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    else:
        # Debug/Development
        app.run(port="5000")
