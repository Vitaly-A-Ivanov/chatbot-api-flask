from classification import classification


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

    # print("users reference : '", nlp.classify(), "'")
    # print("")
    # print("Results in list as comes from Mark: ")
    # print(nlp.returnResultsFromMark())

    nlp.returnResultsFromMark()
    nlp.taxonomy()
    print(nlp.returnResults())

