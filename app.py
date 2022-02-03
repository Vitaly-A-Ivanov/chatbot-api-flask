import os
from TextAnalysis import chatbot

from flask import Flask
from flask import request

# create and configure the app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def run():
    message = request.args.get('message')
    readySubmit = request.args.get('readySubmit')
    topicFound = request.args.get('topicFound')
    fileSubmit = request.args.get('fileSubmit')
    classifiedMsg = request.args.get('classifiedMsg')
    topicSelected = request.args.get('topicSelected')
    topicFinal = request.args.get('topicFinal')
    return chatbot.run(message, readySubmit, topicFound, fileSubmit, classifiedMsg, topicSelected, topicFinal)


if __name__ == '__main__':
    app.run()
