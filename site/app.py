import os
import pickle
import re

from flask import Flask, request, jsonify

# Unpickle the trained classifier and write preprocessor method used
def tokenizer(text):
    return text.split(' ')

def preprocessor(text):
    """ Return a cleaned version of text
    """
    # Remove HTML markup
    text = re.sub('<[^>]*>', '', text)
    # Save emoticons for later appending
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    # Remove any non-word character and append the emoticons,
    # removing the nose character for standarization. Convert to lower case
    text = (re.sub('[\W]+', ' ', text.lower()) + ' ' + ' '.join(emoticons).replace('-', ''))

    return text

tweet_classifier = pickle.load(open('../data/logisticRegression.pkl', 'rb'))

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('html/index.html')


@app.route('/classify', methods=['POST'])
def classify():
    text = request.form.get('text', None)
    assert text is not None

    prob_neg, prob_pos = tweet_classifier.predict_proba([text])[0]
    s = 'Positive' if prob_pos >= prob_neg else 'Negative'
    p = prob_pos if prob_pos >= prob_neg else prob_neg
    return jsonify({
        'sentiment': s,
        'probability': p
    })

app.run()
