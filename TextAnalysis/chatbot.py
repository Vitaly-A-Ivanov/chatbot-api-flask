# -*- coding: utf-8 -*-
import sys
import importlib.util
import random
import json

import pickle
import time

import numpy as np
import os

import nltk
import ssl

from TextAnalysis import FileAnalysis
import TextAnalysis.UserInput as elsie
import TextAnalysis.resourceGathering as rg

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from TextAnalysis.classification import classification

# reducing words to it's stem, for example work, working, worked, works treats as the same word
from nltk.stem import WordNetLemmatizer

# function to load the model that been created in the training script
from tensorflow.keras.models import load_model

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
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
# chatbot response
res = dict()


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
    respond = model.predict(np.array([bow]))[0]
    # threshold to avoid too much uncertainty
    ERROR_THRESHOLD = 0.25
    # enumerates all the results
    results = [[i, r] for i, r in enumerate(respond) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


# function for getting a response
def get_response(intents_list, intents_json):
    result = ''
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def clearAllFlags():
    res['topicFound'] = 'False'
    res['readySubmit'] = 'False'
    res['topicSelected'] = 'False'
    res['fileSubmit'] = 'False'
    res['classifiedMsg'] = ''
    res['fileAnalysed'] = 'False'
    res['topicSelected'] = ''
    res['fileUploaded'] = 'None'
    res['possibleTopics'] = []
    res['topicFinal'] = ''
    res['resourcesProvided'] = 'False'
    res['clarify'] = 'False'
    res['answered'] = 'False'


def run(message, readySubmit, topicWasFound, fileSubmit, classifiedMsg, topicSelected, topicFinal, file, webResources,
        analysedFile, providedResources, isConversationFinished, clarify, answered):
    # final topic name to be sent online to search
    topicToSearchOnline = topicFinal
    res['topicFinal'] = topicToSearchOnline

    # flag to help chatbot to identify if user chose his topic or not
    topicChosen = topicSelected
    res['topicSelected'] = topicChosen

    # flag to avoid repetition of predictions from the intents.json
    topicFound = topicWasFound
    res['topicFound'] = topicFound

    # flag to identify when user accept or not the topic which he wants to look in a text file before submitting it
    readyToSubmit = readySubmit
    res['readySubmit'] = readyToSubmit

    # flag to identify if the user upload the file or not
    fileSubmitted = fileSubmit
    res['fileSubmit'] = fileSubmitted

    # path for a submitted file
    fileUploaded = file
    res['fileUploaded'] = fileUploaded

    # user message
    classifiedMessage = classifiedMsg
    res['classifiedMsg'] = classifiedMessage

    resource = webResources
    res['resource'] = resource

    fileAnalysed = analysedFile
    res['fileAnalysed'] = fileAnalysed

    resourcesProvided = providedResources
    res['resourcesProvided'] = resourcesProvided

    conversationFinished = isConversationFinished
    res['conversationFinished'] = conversationFinished

    isClarify = clarify
    res['isClarify'] = isClarify
    isAnswered = answered
    res['isAnswered'] = isAnswered

    emptyInputResponses = ['Please enter something first... :)',
                           'You did not write anything! Try again!',
                           'Are you joking? I am not so silly, as you may think!',
                           'Oh, man! Seriously?',
                           'Come on! Stop kidding me:(']

    notKnownResponses = ['Sorry?',
                         'Excuse me?',
                         'Pardon?',
                         'Excuse me, could you repeat the question?',
                         'I don’t understand. Could you say it again?',
                         'I didn’t catch that. Would you mind to repeat?',
                         'I’m confused. Could you tell me again?',
                         'I didn’t understand. Could you repeat a little louder?',
                         'I didn’t get you. Could you tell me again?']

    m = message
    message = m.lower()
    res['message'] = message
    userInput = classification(message)

    if not message:
        res['response'] = random.choice(emptyInputResponses)
        return res

    else:

        if topicFound == 'False':
            ints = predict_class(message)
            for i in ints:
                if i['intent'] == 'help' and float(i['probability']) > 0.8:
                    topicFound = 'True'
                    res['topicFound'] = topicFound
                    classifiedMessage = userInput.classify()
                    if classifiedMessage:
                        res['classifiedMsg'] = classifiedMessage
                        res['response'] = "Is '" + classifiedMessage + "' what you looking for?"
                    else:
                        topicFound = 'False'
                        res['topicFound'] = topicFound
                        res['response'] = random.choice(notKnownResponses)
                        break
                elif float(i['probability']) < 0.8:
                    topicFound = 'False'
                    res['topicFound'] = topicFound
                    res['response'] = random.choice(notKnownResponses)
                    break
                else:
                    topicFound = 'False'
                    res['topicFound'] = topicFound
                    res['response'] = get_response(ints, intents)
                    break
            res['readySubmit'] = readyToSubmit
            return res
        else:
            if readyToSubmit == 'False' and fileSubmitted == 'False':
                sid = SentimentIntensityAnalyzer()
                sentiment_score = sid.polarity_scores(message)

                if sentiment_score['pos'] > 0.6:
                    readyToSubmit = 'True'
                    res['readySubmit'] = readyToSubmit
                    res['response'] = "Provide the file please"
                    return res
                if sentiment_score['neg'] > 0.6:
                    topicFound = 'False'
                    readyToSubmit = 'False'
                    res['readySubmit'] = readyToSubmit
                    res['topicFound'] = topicFound
                    classifiedMessage = ""
                    res['classifiedMsg'] = classifiedMessage
                    res['response'] = 'OK, ask me something else again...'
                    return res
                if sentiment_score['neu'] > 0.6:
                    readyToSubmit = 'False'
                    res['readySubmit'] = readyToSubmit
                    res['response'] = 'So, yes or no?'
                    return res
            if fileSubmitted == 'False':
                res['response'] = "Provide the file please"
                return res

            if fileSubmitted == 'True':
                if fileAnalysed == 'False':

                    if isClarify == 'True' and isAnswered == 'False':
                        sid = SentimentIntensityAnalyzer()
                        sentiment_score = sid.polarity_scores(message)
                        if sentiment_score['pos'] > 0.6:
                            res['response'] = 'OK, what topic do you like to search now?'
                            isAnswered = 'True'
                            res['isAnswered'] = isAnswered
                            return res
                        if sentiment_score['neg'] > 0.6:
                            res['response'] = 'Ok, you can ask me something again :}'
                            topicFound = 'False'
                            res['topicFound'] = topicFound
                            readyToSubmit = 'False'
                            res['readySubmit'] = readyToSubmit
                            fileSubmitted = 'False'
                            res['fileSubmit'] = fileSubmitted
                            return res
                        if sentiment_score['neu'] > 0.6:
                            res['response'] = 'So, yes or no?'
                            return res
                    elif isClarify == 'True' and isAnswered == 'True':
                        classifiedMessage = userInput.classify()
                        if classifiedMessage:
                            res['classifiedMsg'] = classifiedMessage
                            res['response'] = "Is '" + classifiedMessage + "' what you looking for?"
                            return res
                        else:
                            res['response'] = random.choice(notKnownResponses)
                            return res
                    else:

                        fileAnalysisResults = FileAnalysis.analyseFile(file,
                                                                       classifiedMessage)
                        if not fileAnalysisResults:
                            if isinstance(fileAnalysisResults, list):
                                res['possibleTopics'] = []

                            res['response'] = 'Sorry, but I could not find `' + classifiedMessage + '` in your ' \
                                                                                                    'file! ' \
                                                                                                    'Try again '
                            'with your '
                            'search!'
                            # topicFound = 'False'
                            # res['topicFound'] = topicFound
                            # readyToSubmit = 'False'
                            # res['readySubmit'] = readyToSubmit
                            # fileSubmitted = 'False'
                            # res['fileSubmit'] = fileSubmitted
                            isClarify = 'True'
                            res['isClarify'] = isClarify
                            return res
                        else:
                            possibleTopics = classification.returnResults(userInput, fileAnalysisResults,
                                                                          classifiedMessage)

                            res['possibleTopics'] = possibleTopics
                            res['response'] = 'Select the most relevant topic for your query'
                            fileAnalysed = 'True'
                            res['fileAnalysed'] = fileAnalysed
                            return res
                else:
                    if resourcesProvided == 'False':
                        res['resource'] = rg.get_resources(topicToSearchOnline)
                        resourcesProvided = 'True'
                        res['resourcesProvided'] = resourcesProvided
                        res['response'] = "Do you need any more help?"
                        return res
                    else:
                        sid = SentimentIntensityAnalyzer()
                        sentiment_score = sid.polarity_scores(message)
                        if sentiment_score['pos'] > 0.6:
                            res['conversationFinished'] = "False"
                            clearAllFlags()
                            res['response'] = 'OK, ask me something else again...'
                            return res
                        if sentiment_score['neg'] > 0.6:
                            res['conversationFinished'] = "True"
                            res['response'] = 'Bye'
                            clearAllFlags()
                            return res
                        if sentiment_score['neu'] > 0.6:
                            res['response'] = 'So, yes or no?'
                            return res

            else:
                clearAllFlags()
                res['response'] = 'Ok, you can ask me something again :}'
                return res
