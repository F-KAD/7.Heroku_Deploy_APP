import spacy
from flask import Flask, request, jsonify
from nltk.stem import PorterStemmer
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
import tensorflow as tf
from keras import backend as K

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
model = None
tokenizer = None

def load_sentiment_model():
    global model
    if model is None:
        model = load_model("model_LSTM_Stem_Glove_Emb_Final_Sentiment_Analysis")

def load_tokenizer():
    global tokenizer
    if tokenizer is None:
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

def tweet_clean(tweet):
    clean = " ".join([PorterStemmer().stem(token.text) for token in nlp(tweet)])
    return clean

def tweet_padded(tweet):
    twt_clean = tweet_clean(tweet)
    padded = pad_sequences(tokenizer.texts_to_sequences([twt_clean]), maxlen=50, padding="post", truncating="post")
    return padded

def tweet_predict(tweet):
    twt_padded = tweet_padded(tweet)
    pred = model.predict(twt_padded)[0][0]
    K.clear_session()  # Libérer la mémoire utilisée par Keras
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
            load_sentiment_model()
            load_tokenizer()
            pred = tweet_predict(tweet)
            sentiment = tweet_sentiment(pred)
            return jsonify({'prediction': pred, 'sentiment': sentiment}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No tweet provided'}), 400

if __name__ == "__main__":
    app.run()
