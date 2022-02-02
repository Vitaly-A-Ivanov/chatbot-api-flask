# -*- coding: utf-8 -*-
import importlib.util
import random
import sys
import json

import pickle
import time

import numpy as np
import os

import nltk

import FileAnalysis
import UserInput as elsie
import resourceGathering as rg

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from classification import classification

# reducing words to it's stem, for example work, working, worked, works treats as the same word
from nltk.stem import WordNetLemmatizer

# function to load the model that been created in the training script
from tensorflow.keras.models import load_model

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('vader_lexicon')

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# lemmatize individual words
lemmatizer = WordNetLemmatizer()
# reads the content of the json file as text and in the result getting json object
intents = json.loads(open('intents.json').read())
# load all prepared files in the training script
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

JSONEncoder = json.JSONEncoder()
JSONDecoder = json.JSONDecoder()


# function for cleaning up the sentences
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


# function for getting the bag of words.
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


# function for predicting the class based on the sentences (result based on a bag of words)
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    # threshold to avoid too much uncertainty
    ERROR_THRESHOLD = 0.25
    # enumerates all the results
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


# function for getting a response
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


# Decoded variables passed from PHP
variables = JSONDecoder.decode(sys.argv[1])
res = dict()
# helps to avoid repetition of predictions from the intents.json
topicFound = variables[0]['topicFound']
res['topicFound'] = variables[0]['topicFound']
# helps to identify when user accept or not the topic which he wants to look in a text file
readyToSubmit = variables[0]['readySubmit']
res['readySubmit'] = variables[0]['readySubmit']
# helps to identify the user upload the file or not before submitting it
fileSubmitted = variables[0]['fileSubmit']
res['fileSubmit'] = variables[0]['fileSubmit']
classifiedMessage = variables[0]['classifiedMsg']
res['classifiedMsg'] = variables[0]['classifiedMsg']

emptyInputResponses = ['Please enter something first... :)',
                       'You did not write anything! Try again!',
                       'Are you joking? I am not so silly, as you may think!',
                       'Oh, man! Seriously?',
                       'Come on! Stop kidding me:(']

notKnownResponses = ['Sorry?',
                     'Excuse me?',
                     'Pardon?',
                     'Excuse me, could you repeat the question?',
                     'I’m sorry, I don’t understand. Could you say it again?',
                     'I’m sorry, I didn’t catch that. Would you mind speaking more slowly?',
                     'I’m confused. Could you tell me again?',
                     'I’m sorry, I didn’t understand. Could you repeat a little louder, please?',
                     'I didn’t hear you. Please could you tell me again?']

m = variables[0]['message']
message = m.lower()
userInput = classification(message)

if not message:
    res['response'] = random.choice(emptyInputResponses)
    print(JSONEncoder.encode(res))
else:
    if not topicFound:
        ints = predict_class(message)
        for i in ints:
            if i['intent'] == 'help' and float(i['probability']) > 0.8:
                topicFound = 'True'
                res['topicFound'] = topicFound
                classifiedMessage = userInput.classify()
                res['classifiedMsg'] = classifiedMessage
                res['response'] = "Is '" + classifiedMessage + "' what you looking for?"
                break
            elif float(i['probability']) < 0.8:
                res['topicFound'] = topicFound
                res['response'] = random.choice(notKnownResponses)
                break
            else:
                res['topicFound'] = topicFound
                res['response'] = get_response(ints, intents)
                break
        res['readySubmit'] = readyToSubmit
        print(JSONEncoder.encode(res))
    else:
        if not readyToSubmit or not fileSubmitted:
            sid = SentimentIntensityAnalyzer()
            sentiment_score = sid.polarity_scores(message)

            if sentiment_score['pos'] > 0.6:
                if fileSubmitted:
                    fileAnalysisResults = FileAnalysis.analyseFile('pdf_files/Individual Neurons.pdf',
                                                                   classifiedMessage)
                    if not fileAnalysisResults:
                        res['response'] = 'Sorry, but I could not find `' + classifiedMessage + '` in your ' \
                                                                                                'file! ' \
                                                                                                'Please ' \
                                                                                                'try again '
                        'with your '
                        'search!'
                        topicFound = 'False'
                        res['topicFound'] = topicFound
                        readyToSubmit = 'False'
                        res['readyToSubmit'] = readyToSubmit
                        print(JSONEncoder.encode(res))
                    else:
                        # will need to return the user's selected topic as a string
                        topic = elsie.main(fileAnalysisResults)
                        res['resource'] = rg.get_resources(topic)
                        res['response'] = "Do you need any more help?"
                        topicFound = 'False'
                        res['topicFound'] = topicFound
                        readyToSubmit = 'False'
                        res['readyToSubmit'] = readyToSubmit
                        print(JSONEncoder.encode(res))
                else:
                    readyToSubmit = 'True'
                    res['readyToSubmit'] = readyToSubmit
                    res['response'] = "Provide the file please"
                    print(JSONEncoder.encode(res))

                if sentiment_score['neg'] > 0.6:
                    topicFound = 'False'
                    res['topicFound'] = topicFound
                    res['response'] = 'OK, ask me something else again...'
                    print(JSONEncoder.encode(res))
                if sentiment_score['neu'] > 0.6:
                    res['response'] = 'So, yes or no?'
                    print(JSONEncoder.encode(res))
            else:
                topicFound = 'False'
                res['topicFound'] = topicFound
                readyToSubmit = 'False'
                res['readySubmit'] = readyToSubmit
                res['response'] = 'Ok, you can ask me something again :}'
                print(JSONEncoder.encode(res))


