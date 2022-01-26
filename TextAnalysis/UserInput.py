#from main import analyseFile

# takes the file path/keywords (Mark) and returns the list


def main(list_items):
    for i in list_items:
        print(i)

    option = int(input("Which topic do you need help with? "
                       "Please select the corresponding number: "))

    while option != 0:
        if option == 1:
            # chosen keyword 1
            print("You have chosen Neurons")
        elif option == 2:
            # chosen keyword 2
            print("You have chosen Simulated Neurons")
        elif option == 3:
            # chosen keyword 3
            print("You have chosen Point Neurons")
        else:
            print("Please select a topic")

        option = int(input("Select your topic:"))



# testing

# testFilePath = "files/Cognitive Neural Networks.pdf"
#
# main(analyseFile(testFilePath, "(ai|artificial intelligence)"))

