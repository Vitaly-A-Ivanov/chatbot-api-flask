from TextAnalysis.file.BaseFile import BaseFile
from TextAnalysis.file.PDF import PDF
from typing import Union
import re


class FileAnalysis:
    """
    The FileAnalysis class analyses files for keyword(s), returning a list of 'sentences' containing those keyword(s).
    """

    # A regex expression to find keywords in the 'sentences'
    __REGEX_FORMAT_KEYWORDS = "(^|\s+|[^A-Za-z0-9]){}($|\s+|[^A-Za-z0-9])"

    # A regex expression to find 'sentences'
    __REGEX_SENTENCE_FINDER = "(\s*)((\n?[\.\?\!]\s*\n?)|(\n([A-Za-z0-9][\.\)]|[–•])\s*|\n\s*[A-Z]))(\s*)"
    # A regex expression to replace the found 'sentence' ending with two new lines
    __REGEX_SENTENCE_SEPARATOR = r"\3\n\n\4"
    # A regex expression to split the text into 'sentences' (sentences separated by two or more new lines)
    __REGEX_SENTENCE_SPLITTER = "(\n{2,})"

    # A regex expression to find single new lines in a 'sentence' that need to be replaced with a single space
    __REGEX_SENTENCE_NEW_LINE_FINDER = "(\s*\n\s*)"
    # A regex expression to find list item prefixes in a 'sentence' that need to be removed
    __REGEX_SENTENCE_LIST_ITEM_PREFIX_FINDER = "^([A-Za-z0-9][\.\)]|[–•§])\s*"
    # A regex expression to find a 'sentence' with certain suffixes that should be filtered out
    __REGEX_SENTENCE_SUFFIX_FILTER = "[\?:]$"

    # A regex expression to indicate a 'sentence' only contains a keyword
    __REGEX_SENTENCE_KEYWORD_FILTER = "^{}$"
    # A regex expression to find certain words in 'sentences' that indicate the sentence should be filtered
    __REGEX_SEARCH_RESULTS_FILTER = __REGEX_FORMAT_KEYWORDS.format("(lecture[s]{0,1}|acknowledgement)")

    def __init__(self, file: BaseFile):
        """
        The class constructor.

        :param file: The file to analyse.
        :raises TypeError: When the file parameter is not a 'BaseFile' object.
        """

        # If the given file is not of type 'BaseFile', an error will be raised
        if not isinstance(file, BaseFile):
            raise TypeError("File must be of type 'BaseFile', not '{}'".format(file.__class__.__name__))

        self.__file = file
        self.__text = self.__getCleanedText()
        self.__previousSearchResults = None

    def getFile(self) -> BaseFile:
        """
        Returns the file being analysed.

        :return: The file being analysed.
        """

        return self.__file

    def getPreviousSearchResults(self) -> Union[list[str], None]:
        """
        Returns the the results of the last search.

        :return: The results of the last search, or None if a search hasn't been done.
        """

        return self.__previousSearchResults

    def search(self, regex: str, caseSensitive: bool=False) -> list[str]:
        """
        Searches the file for the given keyword(s).

        :param regex: The keyword(s) to search for.
        :param caseSensitive: Whether or not the keyword(s) must match cases.
        :return: The list of 'sentences' containing the keyword(s).
        """

        # Updates the regex to make sure the keyword(s) are whole words
        regex = FileAnalysis.__REGEX_FORMAT_KEYWORDS.format(regex)
        # Splits the file's text into 'sentences'
        fileSentences = self.__splitTextIntoSentences()
        # The list of 'sentences' containing keyword(s)
        self.__previousSearchResults = []

        # Loops through the file's sentences
        for sentence in fileSentences:
            # Replace new lines (and any extra spaces surrounding them) with a single space
            sentence = self.__cleanSentence(sentence)

            # Searches the 'sentence' for the keyword(s)
            if caseSensitive:
                results = re.search(regex, sentence)
            else:
                results = re.search(regex, sentence, re.IGNORECASE)

            # Adds the 'sentence' to the list of matched sentences if any keyword(s) were found
            if results != None and not self.__shouldFilterSentence(sentence, regex, caseSensitive):
                self.__previousSearchResults.append(sentence)

        # Sort the matched 'sentences' in ascending order of length
        self.__removeDuplicatesFromSearchResults()
        self.__previousSearchResults.sort(key=len, reverse=True)

        return self.__previousSearchResults

    def __splitTextIntoSentences(self) -> list[str]:
        """
        Splits the text from the file into 'sentences'.

        :return: A list of 'sentences'.
        """

        return re.split(FileAnalysis.__REGEX_SENTENCE_SPLITTER, re.sub(FileAnalysis.__REGEX_SENTENCE_FINDER, FileAnalysis.__REGEX_SENTENCE_SEPARATOR, self.__text.strip()))

    def __getCleanedText(self) -> str:
        """
        Cleans the text from the file.

        :return: The cleaned text.
        """

        return self.__file.getText().strip()

    @staticmethod
    def __cleanSentence(sentence) -> str:
        """
        Cleans the given 'sentence'.

        :return: The cleaned 'sentence'.
        """

        return re.sub(FileAnalysis.__REGEX_SENTENCE_NEW_LINE_FINDER, " ", re.sub(FileAnalysis.__REGEX_SENTENCE_LIST_ITEM_PREFIX_FINDER, "", sentence.strip()))

    @staticmethod
    def __shouldFilterSentence(sentence: str, keywords: str, caseSensitive: bool=False) -> bool:
        """
        Returns whether or not the given 'sentence' should be filtered out of the matched 'sentences'.

        :return: Whether or not the given 'sentence' should be filtered out of the matched 'sentences'.
        """

        if caseSensitive:
            flag = 0
        else:
            flag = re.IGNORECASE

        if re.search(FileAnalysis.__REGEX_SENTENCE_KEYWORD_FILTER.format(keywords), sentence, flag) != None\
            or re.search(FileAnalysis.__REGEX_SEARCH_RESULTS_FILTER, sentence, flag) != None\
            or re.search(FileAnalysis.__REGEX_SENTENCE_SUFFIX_FILTER, sentence, flag) != None:

            return True

        return False

    def __removeDuplicatesFromSearchResults(self) -> None:
        """
        Removes any duplicate sentences from the search results (case-insensitive).
        """

        lowercaseSearchResults = [sentence.lower() for sentence in self.__previousSearchResults]
        filteredSearchResults = []

        for sentence in self.__previousSearchResults:
            if sentence.lower() in lowercaseSearchResults:
                filteredSearchResults.append(sentence)
                lowercaseSearchResults = [s for s in lowercaseSearchResults if s != sentence.lower()]

            if len(lowercaseSearchResults) == 0:
                break

        self.__previousSearchResults = filteredSearchResults



def analyseFile(filePath: str, keywords: str) -> Union[list[str], None]:
    """
    Analyses the file at the given path for 'sentences' containing any of the given keyword(s).

    :param filePath: The path of the file to analyse.
    :param keywords: The keyword(s) to find (can be a regular string or a regex string).
    :return: The list of 'sentences' containing the keyword(s), or None if a file couldn't be found at the given path.
    """

    # If no file was found
    if not BaseFile.isFile(filePath):
        print("File Not Found!")

        return None
    # If no keywords were provided
    elif keywords == None or (isinstance(keywords, str) and len(keywords.strip()) == 0):
        print("No keywords provided!")

        return None

    keywords = str(keywords)
    extension = BaseFile.getFileExtension(filePath)
    file = None

    # If the file is a PDF
    if extension == PDF.getFileTypeExtension():
        file = PDF(filePath)

    # If a valid file wasn't found
    if file == None:
        print("Invalid file type")

        return None
    # Returns the list of 'sentences' containing the keyword(s)
    else:
        fileAnalysis = FileAnalysis(file)

        # Closes the file as it is no longer needed
        file.close()

        return fileAnalysis.search(keywords)
