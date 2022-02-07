import en_core_web_sm
from spacy.matcher import DependencyMatcher

# Load the model en_core_web_sm of English for vocabulary, syntax & entities
classifier = en_core_web_sm.load()
nlp = en_core_web_sm.load()

stopwords = classifier.Defaults.stop_words

## IMPORT MARK'S FUNCTIONS TO ITERATE THE ARRAY GIVER FROM THE FILE_ANALYSIS
from TextAnalysis import FileAnalysis

# Create an array for all the nouns in the input
nouns = []

# Create an array for all the verbs in the input
verbs = []

# Create an array for all the adjectives in the input
adjectives = []

# Create an array to combine adjectives and nouns from the input
chunks = []

fileResults = []

lemmatized_classifiedMessage = ""

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
            return None

    def returnResultsFromMark(self, results, keyword):
        # THE KEYWORD TO CHECK THE DOCUMENT
        keyword = self.classify()
        #
        # # UNFILTERED RESULTS OF THE DOCUMENT BASED ON THE KEYWORD
        # fileAnalysisResults = FileAnalysis.analyseFile('pdf_files/Individual Neurons.pdf',
        #                                                classifiedMessage)

        # SORT THE RESULTS
        results.sort()

        # LOWECASE THE RESULTS FOR BETTER ITERATION
        for i in range(len(results)):
            results[i] = results[i].lower()

        return results, keyword

    def taxonomy(self, results):
        #  STORE THE SORTED VERSION FROM MARK'S FILE
        # results = self.returnResultsFromMark()

        # print("UNFILTERED RESULTS: ", results[0])  # TODO remove this line after demo
        # print("")

        # GET THE KEYWORD FROM THE ARRAY
        classifiedMessage = results[1]
        # ADD META DATA TO KEYWORD WITH SPACY ENCODE
        classifiedMessage = nlp(classifiedMessage)

        # LEMMATIZE THE KEYWORD FOR BETTER MATCH WITH THE RESULTS
        lemmatized_classifiedMessage = " ".join([token.lemma_ for token in classifiedMessage])

        # print("LEMMATIZED USER INPUT: ",
        #       lemmatized_classifiedMessage)  # TODO remove this line after demo
        # print("")

        # LIST TO HOLD THE FILTERED RESULTS
        filtered_lemmatized_sentence = []

        # LIST TO HOLD THE FILTERED RESULTS AFTER LEMMATIZATION
        filtered_lemmatized_sentence_after_lemma = []

        # FOR EACH SENTENCE CREATES A NEW VERSION OF THE SENTENCE WITH THE ROOT WORDS
        for text in range(len(results[0])):
            sentence = classifier(results[0][text])
            lemmatized_sentence = ""
            for word in sentence:
                lemmatized_sentence = lemmatized_sentence + " " + word.lemma_

            # ADD THE NEW LEMMATIZED SENTENCE IN THE LIST
            filtered_lemmatized_sentence.append(lemmatized_sentence)

        # print("LEMMATIZED SENTENCES: ", filtered_lemmatized_sentence)  # TODO remove this line after demo
        # print("")

        # CREATE NOUN CHUNCKS FROM THE SENTENCES
        for text in range(len(filtered_lemmatized_sentence)):
            sentence = classifier(filtered_lemmatized_sentence[text])

            # DIVIDE THE SENTENCE INTO CHUNKS AND APPENDED TO THE LIST
            filtered_lemmatized_sentence_after_lemma.append((list(sentence.noun_chunks)))

        # SORT THE LIST
        filtered_lemmatized_sentence_after_lemma.sort()
        # print("NOUN CHUNCKS: ", filtered_lemmatized_sentence_after_lemma)  # TODO remove this line after demo
        # print("")

        # CREATE CHUNCKS OF WORDS RELATED TO THE KEYWORD
        chuncks_related_to_keyword = []

        # ITERATE THE LEMMATIZED LIST
        for row in filtered_lemmatized_sentence_after_lemma:

            # CHECK IF THE KEYWORD ARREARS IN THE CHUNCK
            for chunck in row:
                if lemmatized_classifiedMessage in str(chunck):
                    chuncks_related_to_keyword.append(chunck)

        # print("CHUNCKS WITH THE KEYWORD INCLUDED", chuncks_related_to_keyword)  # TODO remove this line after demo

        # LIST TO HOLD THE CHUNCKS WITH THE RELATED KEYWORD WITHOUT DUPLICATES
        list_without_duplicates = []

        # CHECK FOR COMBINATIONS OF ( ADJECTIVE + NOUN ) OR ( NOUN + NOUN ) AND IGNORE RANDOM WORDS
        for occurrence in chuncks_related_to_keyword:

            chuncks_related_to_keyword_chunck = ""
            chuncks_related_to_keyword_adj = ""
            chuncks_related_to_keyword_noun = ""
            chuncks_related_to_keyword_second_noun = ""

            for word in occurrence:
                if word.pos_ == "ADJ":
                    chuncks_related_to_keyword_adj = word.text
                if word.pos_ == "NOUN":
                    chuncks_related_to_keyword_noun = word.text

            # IF THERE IS A COMBO OF ( ADJECTIVE - NOUN ), JOIN THEM AND ADD INTO THE LIST
            if chuncks_related_to_keyword_adj and chuncks_related_to_keyword_noun:
                chuncks_related_to_keyword_chunck = \
                    chuncks_related_to_keyword_adj + " " + chuncks_related_to_keyword_noun

                list_without_duplicates.append(chuncks_related_to_keyword_chunck)

            chuncks_related_to_keyword_noun = ""
            chuncks_related_to_keyword_second_noun = ""

            # IF THERE IS A COMBO OF ( NOUN - NOUN ), JOIN THEM AND ADD INTO THE LIST
            for word in occurrence:
                if word.pos_ == "NOUN":
                    if not chuncks_related_to_keyword_noun:
                        chuncks_related_to_keyword_noun = word.text
                if word.pos_ == "NOUN":
                    if word.text not in chuncks_related_to_keyword_noun:
                        chuncks_related_to_keyword_second_noun = word.text

            if chuncks_related_to_keyword_noun and chuncks_related_to_keyword_second_noun:
                chuncks_related_to_keyword_chunck = \
                    chuncks_related_to_keyword_noun + " " + chuncks_related_to_keyword_second_noun

                list_without_duplicates.append(chuncks_related_to_keyword_chunck)

        # FINAL SORT
        list_without_duplicates.sort()
        # REMOVE DUPLICATE OCCURRENCES
        list_without_duplicates = list(dict.fromkeys(list_without_duplicates))

        # RETURNED LIST WILL DISPLAYED TO THE USER
        return list_without_duplicates


    def returnResults(self):
       array = self.returnResultsFromMark()

       return self.taxonomy(array)


