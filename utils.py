import re
import io
import numpy as np
from nltk.util import ngrams

def get_vocab(filename):
    lines = [line.rstrip() for line in io.open(filename, encoding='utf8')]
    vocab = dict()

    for line in lines:
        line = line.split(" ")
        if len(line) != 2:  # skip last line
            continue
        [word_index, word] = line
        vocab[word] = word_index

    return vocab

def process_input(review, vocab):
    window_size = 2
    docid = 0
    contexts = []

    review = review.lower()
    review = re.sub(r'[^a-zA-Z0-9\s]', ' ', review)
    tokens = [token for token in review.split(" ") if token in vocab]
    n_grams = list(ngrams(tokens, window_size))

    for ngram_index in range(len(n_grams)):
        context = [docid]
        n_gram = n_grams[ngram_index]

        for word in n_gram:
            word = re.sub("[.,:;'\"!?()]+", "", word.lower())
            context.append(vocab[word])

        contexts.append(context)

    return np.array(contexts)

def get_review_sentiment(review, model, vocab):
    contexts = process_input(review, vocab)

    ctx_amt = 0
    prediction = np.array([0.,0.])
    for ctx in contexts:
        ctx_amt += 1
        w1 = np.array([ctx[1]])
        w2 = np.array([ctx[2]])
        doc = np.array([ctx[0]])

        pred = model.predict([w1, w2, doc])[0]
        prediction[0] = prediction[0] + pred[0]
        prediction[1] = prediction[1] + pred[1]

    review_sentiment = np.argmax(prediction)
    review_confidence = prediction[review_sentiment] / ctx_amt

    review_sentiment = 'positive' if review_sentiment else 'negative'

    return review_sentiment, review_confidence