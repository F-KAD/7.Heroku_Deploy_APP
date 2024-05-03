import spacy
import subprocess
# Installation du modèle spaCy
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])



from flask import Flask, request, jsonify
from nltk.stem import PorterStemmer

from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

from keras.models import load_model
#import tensorflow as tf
#from tensorflow.keras.models import load_model

import pickle

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Charger le tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Charger le modèle
model = load_model("model_LSTM_Stem_Glove_Emb_Final_Sentiment_Analysis")

def tweet_clean(tweet):
    clean = " ".join([PorterStemmer().stem(token.text) for token in nlp(tweet)])
    return clean

def tweet_padded(tweet):
    twt_clean = tweet_clean(tweet)
    padded = pad_sequences(tokenizer.texts_to_sequences([twt_clean]), maxlen=50, padding="post", truncating="post")
    return padded

def tweet_predict(tweet):
    twt_padded = tweet_padded(tweet)
    pred = float(model.predict(twt_padded)[0][0])
    return pred

def tweet_sentiment(pred):
    if pred > 0.5:
        return "Positive"
    else:
        return "Negative"

@app.route("/")
def index():
    return "Welcome to Sentiment Analysis API!"

@app.route("/predict", methods=["GET"])
def predict():
    tweet = request.args.get('tweet')
    if tweet:
        try:
            pred = tweet_predict(tweet)
            sentiment = tweet_sentiment(pred)
            return jsonify({'prediction': pred, 'sentiment': sentiment}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No tweet provided'}), 400

#if __name__ == "__main__":
    #app.run(port=8000, debug=True)
 #   app.run()

#if __name__ == "__main__":
   # port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    app.run()
