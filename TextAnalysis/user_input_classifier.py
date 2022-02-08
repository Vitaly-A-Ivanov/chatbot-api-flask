from classification import classification
from TextAnalysis import FileAnalysis


"""
Creates a a loop to accent a user's input until the user terminates chooses to terminate it
Creates an instance of the classification class
Calls the functions from the classification class
"""


while True:
    user = input("You:")
    if user == "exit":
        break

    nlp = classification(user)
    classifiedMessage = nlp.classify()
    fileAnalysisResults = FileAnalysis.analyseFile('pdf_files/Individual Neurons.pdf',
                                                   classifiedMessage)

    # results = nlp.returnResultsFromMark(fileAnalysisResults, classifiedMessage)
    possibleTopics = nlp.returnResults(fileAnalysisResults, classifiedMessage)
    print(possibleTopics)
