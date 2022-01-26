import en_core_web_sm

# Load the model en_core_web_sm of English for vocabulary, syntax & entities
classifier = en_core_web_sm.load()

# Create an array for all the nouns in the input
nouns = []

# Create an array for all the verbs in the input
verbs = []

# Create an array for all the adjectives in the input
adjectives = []

# Create an array to combine adjectives and nouns from the input
chunks = []


""""
Create a class to initialise the user input and use classification
operators to analyse the user input
"""


class classification:
    """
    Constructor for the classification class
    :parameter - userInput
    """

    def __init__(self, userInput):
        self.userInput = userInput

    """
    Function to return the user input
    """

    def returnInput(self):
        return self.userInput

    """
    Run the the user input throught the classifier param from spacy
    :return the text
    """

    def run_classifier(self):
        classified_input = classifier(self.userInput)
        return classified_input

    """
    Function to tokenize the user input
    :returns a tokenized list of the input
    """

    def text_tokenize(self):

        token_list = []

        for token in self.run_classifier():
            token_list.append(token.text)
        return token_list

    """
    Function to clear the input from the stop words (“a”, “the”, “is”, “are” and etc)
    :returns a filtered list with no stop words
    """

    def clean_stop_words(self):

        filtered_sent = []
        for word in self.run_classifier():
            if not word.is_stop:
                filtered_sent.append(word)
        return filtered_sent

    """
    Function to lemmatize the user input and classify each word by utilising a for loop to store the verbs,
    adjectives and nouns to  their corresponding lists. Checks in the user input if there is an adjective
    and a noun and calls a function to store them as a chunk
    :params - noun, adj (bool)
    :params - noun_text, adj_text (string)
    """

    def text_lemmatizer(self):

        noun = False
        adj = False
        noun_text = ""
        adj_text = ""

        for word in self.run_classifier():
            # print(word.text, word.pos_)
            if word.pos_ == "VERB":
                verbs.append(word.text)
            if word.pos_ == "ADJ":
                adj = True
                adj_text = word.text
                adjectives.append(word.text)
            if word.pos_ == "NOUN":
                noun = True
                noun_text = word.text
                nouns.append(word.text)

        if adj and noun:
            self.create_chunks(adj_text, noun_text)

    """
    Function to save the adjective and the noun into the list
    """

    def create_chunks(self, noun, adj):
        chunks.append(noun + " " + adj)

    """
    Prints the list of the nouns
    """

    def print_nouns(self):
        return nouns

    """
    Prints the list of the verbs
    """

    def print_verbs(self):
        return verbs

    """
    Prints the list of the adjectives
    """

    def print_adjectives(self):
        return adjectives

    """
    Prints the list of the chunks
    """

    def print_chunks(self):
        return chunks

    """
    function to check check the list for the most accurate response to the user
    """

    def classify(self):

        self.text_lemmatizer()
        if chunks:
            return chunks[-1]
        elif nouns:
            return nouns[-1]
        elif adjectives:
            return nouns[-1]
        else:
            return
