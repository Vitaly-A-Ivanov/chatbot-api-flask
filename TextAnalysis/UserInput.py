def main(searchResult):

    # If searchResult is not a list or is empty
    if not isinstance(searchResult, list) or len(searchResult) == 0:
        return None
    # will not return any results

    # Print each item in searchResult with their corresponding index
    for i in range(len(searchResult)):
        print("[" + str(i) + "] " + str(searchResult[i]))

    # Keep asking the user for valid corresponding number,
    # an integer and has a valid index in searchResult
    while True:
        # Try to convert the user's response into an integer
        try:
            response = int(input("Which topic do you need help with? " + "Please select a number from the list above: "))
        # If the user's response cannot be converted to an integer,
        # set the response to -1 (out of bounds)
        except:
            response = -1

        # If the response was a valid index, return the item in
        # searchResult at the corresponding index
        if 0 <= response < len(searchResult):
            return searchResult[response]
        # returns a list of responses

        # Otherwise, inform the user their input was invalid,
        # it will loop back to the main asking them to re enter
        else:
            print("Invalid number, please try again!")





# #from main import analyseFile
#
#
# def main(list_items):
#     for i in list_items:
#         print(i)
#
#     option = int(input("Which topic do you need help with? "
#                        "Please select the corresponding number: "))
#
#     while option != 0:
#         if option == 1:
#             # chosen keyword 1
#             print("You have chosen Neurons")
#         elif option == 2:
#             # chosen keyword 2
#             print("You have chosen Simulated Neurons")
#         elif option == 3:
#             # chosen keyword 3
#             print("You have chosen Point Neurons")
#         else:
#             print("Please select a topic")
#
#         option = int(input("Select your topic:"))

