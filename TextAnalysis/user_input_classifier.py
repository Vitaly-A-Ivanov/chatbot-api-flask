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

    userInput = classification(user)

    print(userInput.returnInput())
    print(" ")

    # print(userInput.text_tokenize())
    # print(" ")

    userInput.text_lemmatizer()
    print(" ")

    userInput.clean_stop_words()
    print(" ")

    userInput.print_verbs()
    print(" ")

    userInput.print_nouns()
    print(" ")

    userInput.print_adjectives()
    print(" ")

    userInput.print_chunks()
