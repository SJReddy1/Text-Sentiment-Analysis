print("\nLoading the app....")
print("Please wait....\n")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import urllib.request as request
from os import path
import os




if not path.exists('./model'):
    os.makedirs('./model') 


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing import sequence
import numpy as np
import pickle

with open('./model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load json and create model
json_file = open('./model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("./model/model.h5")

def predict_response(response):
    response = tokenizer.texts_to_sequences(response)
    response = sequence.pad_sequences(response, maxlen=48)
    probs = np.around(model.predict(response),decimals=2)
    pred = np.argmax(probs)
    #print(probs)
    #print(pred)
    if pred == 0:
        tag = 'Very Negative'
        tag_prob = probs[0,0]
        sent_prob = np.sum(probs[0,:2])
    elif pred == 1:
        tag = 'Negative'
        tag_prob = probs[0,1]
        sent_prob = np.sum(probs[0,:2])
    elif pred == 2:
        tag = 'Neutral'
        tag_prob = probs[0,2]
        sent_prob = probs[0,2]        
    elif pred == 3:
        tag = 'Positive'
        tag_prob = probs[0,3]
        sent_prob = np.sum(probs[0,3:])
    elif pred == 4:
        tag = 'Very Positive'
        tag_prob = probs[0,4]
        sent_prob = np.sum(probs[0,3:])
    return tag, tag_prob, sent_prob
