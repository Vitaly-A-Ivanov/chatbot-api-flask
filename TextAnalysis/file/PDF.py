# If this module is run directly, import BaseFile normally
if __name__ == "__main__":
    from BaseFile import BaseFile
# If this module isn't run directly, import BaseFile from the package
else:
    from .BaseFile import BaseFile

from typing import Union
from pdfplumber.pdf import Page
import pdfplumber


class PDF(BaseFile):
    """
    The PDF class represents a PDF file, providing methods to retrieve the text from the file.
    """

    # The name of the file type
    __FILE_TYPE = "PDF"
    # The extension of the file type
    __FILE_EXTENSION = ".pdf"
    # The mode the file will be opened with
    __MODE = "rb"

    def __init__(self, filePath: str):
        """
        The class constructor.

        :param filePath: The path to the PDF file.
        """

        super().__init__(filePath, PDF.getFileType(), PDF.getFileTypeExtension(), PDF.getFileMode())

        self.__PDF_PLUMBER = pdfplumber.open(self.getOpenedFile())

    def getTotalPages(self) -> int:
        """
        Returns the number of pages in the PDF.

        :return: The number of pages in the PDF.
        """

        return len(self.getPages())

    def isPage(self, pageNum: int) -> bool:
        """
        Returns whether or not the given page number is within range of the pages in the PDF.

        :param pageNum: The page number.
        :return: Whether or not the page exists.
        """

        return 1 <= pageNum <= self.getTotalPages()

    def getPages(self) -> list[Page]:
        """
        Returns a list of the pages in the PDF.

        :return: The list of pages in the PDF.
        """

        return self.__PDF_PLUMBER.pages

    def getPage(self, pageNum: int) -> Union[Page, None]:
        """
        Returns the page from the PDF with the given page number.

        :param pageNum: The page number.
        :return: The page.
        """

        if self.isPage(pageNum):
            return self.getPages()[pageNum - 1]

        return None

    def getTextFromPage(self, pageNum: int) -> Union[str, None]:
        """
        Returns the text from the page in the PDF with the given page number.

        :param pageNum: The page number.
        :return: The text from the page.
        """

        if self.isPage(pageNum):
            return self.getPage(pageNum).extract_text()

        return None

    def getTextFromPages(self) -> list[str]:
        """
        Returns a list of text from each page in the PDF.

        :return: The list of text from each page in the PDF.
        """

        return [self.getTextFromPage(pageNum) for pageNum in range(1, self.getTotalPages() + 1)]

    def getText(self) -> str:
        """
        Returns all the text in the PDF.

        :return: All the text in the PDF.
        """

        return "\n\n".join(self.getTextFromPages())

    def close(self) -> None:
        """
        Closes the PDF if it is opened.
        """

        if not super().isClosed():
            self.__PDF_PLUMBER.close()
            super().close()

    @staticmethod
    def getFileType() -> str:
        """
        Returns the name of this file type.

        :return: The name of this file type.
        """

        return PDF.__FILE_TYPE

    @staticmethod
    def getFileTypeExtension() -> str:
        """
        Returns the extension of this file type.

        :return: The extension of this file type.
        """

        return PDF.__FILE_EXTENSION

    @staticmethod
    def getFileMode() -> str:
        """
        Returns the mode this file type will be opened with.

        :return: The mode this file type will be opened with.
        """

        return PDF.__MODE