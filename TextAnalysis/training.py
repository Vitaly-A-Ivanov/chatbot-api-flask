import random
import json
# for serialization
import pickle
import numpy as np
import warnings
import os
import nltk

# reducing words to it's stem, for example work, working, worked, works treats as the same word
from nltk.stem import WordNetLemmatizer

# Neural network models, layers and optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# lemmatize individual words
lemmatizer = WordNetLemmatizer()
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
#######################################################
# Load Training Data
#######################################################

# reads the content of the json file as text and in the result getting json object
intents = json.loads(open('intents.json').read())

# empty word list
words = []

# empty tags list
classes = []

# empty combination list
documents = []
ignore_letters = ['?', '!', '.', ',']

# Iterate over the intents
for intent in intents['intents']:
    # Iterate over the sub-categories 'patterns' inside the intents
    for pattern in intent['patterns']:
        # Tokenize each pattern
        word_list = nltk.word_tokenize(pattern)
        # Add tokens/collection of words to the 'word' list
        words.extend(word_list)
        # Add tokens and it's tags as a tuple to the documents, so its know to which tags the word belongs
        documents.append((word_list, intent['tag']))
        # check if the classes are not the classes lit, so it can't be added twice
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# displays the actual result from the loop above ( testing only)
# print(documents)

# lemmatize the words
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
# eliminates the duplicates
words = sorted(set(words))

# displays the list of lemmattized words ( testing only)
# print(words)

# eliminates the duplicates
classes = sorted(set(classes))
# saves words in the files for the later usage
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


#######################################################
# Data preprocessing, Prepare Training Data
#######################################################

# Concept below is to represent all words as are numerical values

# "Bag of Words implementation".
# Sets individual words indices/values to either 0 or 1 depending if it's occurring in the particular pattern.
training = []
# template of zero's
output_empty = [0] * len(classes)
# Convert the document data to the training list in order to train the neural network
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

#######################################################
# Building Neural network model
#######################################################

# Creates a simple sequential model
model = Sequential()
# Creates the input layer (Dense layer with 128 neurones and
# an input shape that is dependent on the size of the training data)
# Activation function to be a rectified linear unit (relu)
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
# Prevents over fitting
model.add(Dropout(0.5))
# Creates the input layer (Dense layer with 64 neurones)
# Activation function to be a rectified linear unit (relu)
model.add(Dense(64, activation='relu'))
# Prevents over fitting
model.add(Dropout(0.5))
# Creates the input layer (Dense layer with the many neurons as classes)
# Activation function is to be a softmax function
model.add(Dense(len(train_y[0]), activation='softmax'))
# Stochastic gradient descent optimizer.
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# model compiling
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
# Feeding the model with prepared data, 200 times with the medium amount of information(verbose = 1)
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbotmodel.h5', hist)
print("Done")
