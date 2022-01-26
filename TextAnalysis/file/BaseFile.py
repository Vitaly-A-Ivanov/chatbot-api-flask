from typing import Union
from abc import ABC, abstractmethod
import io
import os


class BaseFile(ABC):
    """
    The BaseFile class is an abstract class representing a generic file, storing and providing additional basic
    information about the file that the default IO classes don't.

    Sub-classes of this class should be those of specific file types that can manage that file type more specifically.

    The file must exist at the given path otherwise an error will be thrown as this class doesn't manage creating or
    editing files, rather getting information about a given file that already exists.
    """

    # The different modes a file can be opened with
    __MODES = [
        "r", "rt", "rb", # Read
        # This class only supports reading the file so the below modes won't be accepted:
        #"a", "at", "ab", # Append
        #"w", "wt", "wb", # Write
        #"x", "xt", "xb"  # Create
    ]

    # The default mode a file will be opened with if one isn't, or an invalid one is, given
    __DEFAULT_MODE = __MODES[0]

    def __init__(self, filePath: str, fileType: str, fileExtension: str, fileMode: str=__DEFAULT_MODE):
        """
        The class constructor.

        :param filePath: The path of the file.
        :param fileType: The type of the file.
        :param fileExtension: The file type's extension.
        :param fileMode: The mode the file will be opened with. See BaseFile.__MODES for a list of valid modes.
        :raises FileNotFoundError: When a file couldn't be found at the given file path.
        :raises TypeError: When the file at the given file path is an invalid file type.
        """

        # The absolute file path of the file path given, as relative paths may be used
        absolutePath = BaseFile.getAbsoluteFilePath(filePath)

        # Throws a FileNotFoundError if there isn't a file at the given path
        if not BaseFile.isFile(absolutePath):
            raise FileNotFoundError("No file found at {}".format(absolutePath))
        # Throws a TypeError if the file is an invalid file type
        elif BaseFile.getFileExtension(absolutePath).lower() != fileExtension.lower():
            raise TypeError("The specified file is not a {}".format(fileType))

        self.__PATH = absolutePath
        self.__DIRECTORY = BaseFile.getFileDirectory(self.__PATH)
        self.__FILENAME = BaseFile.getFileFilename(self.__PATH)
        self.__NAME = BaseFile.getFileName(self.__PATH)
        self.__EXTENSION = fileExtension
        self.__TYPE = fileType

        # Checks if the given mode is valid, otherwise the default mode will be used
        if BaseFile.isMode(fileMode):
            self.__MODE = fileMode.lower()
        else:
            self.__MODE = BaseFile.__DEFAULT_MODE

        self.__OPENED_FILE = open(self.__PATH, self.__MODE)

    @abstractmethod
    def getText(self) -> str:
        """
        Returns the text from the file.

        :return: The text from the file.
        """

        pass

    def getPath(self) -> str:
        """
        Returns the path of the file.

        :return: The path of the file.
        """

        return self.__PATH

    def getDirectory(self) -> str:
        """
        Returns the directory path the file is in.

        :return: The directory path the file is in.
        """

        return self.__DIRECTORY

    def getFilename(self) -> str:
        """
        Returns the file's name with the extension.

        :return: The file's name with the extension.
        """

        return self.__FILENAME

    def getName(self) -> str:
        """
        Returns the file's name without the extension.

        :return: The file's name without the extension.
        """

        return self.__NAME

    def getExtension(self) -> str:
        """
        Returns the file's extension.

        :return: The file's extension.
        """

        return self.__EXTENSION

    def getType(self) -> str:
        """
        Returns the file's type.

        :return: The file's type.
        """

        return self.__TYPE

    def getMode(self) -> str:
        """
        Returns the mode the file is opened with.

        :return: The mode the file is opened with.
        """

        return self.__MODE

    def getOpenedFile(self) -> io:
        """
        Returns the opened file.

        :return: The IO object the file is opened with.
        """

        return self.__OPENED_FILE

    def close(self) -> None:
        """
        Closes the file if it is opened.
        """

        if not self.isClosed():
            self.getOpenedFile().close()

    def isClosed(self) -> bool:
        """
        Returns whether or not the file is closed.

        :return: Whether or not the file is closed.
        """

        return self.getOpenedFile().closed

    @staticmethod
    def getAbsoluteFilePath(filePath: str) -> Union[str, None]:
        """
        Returns the absolute file path of the given file path.

        :return: The absolute file path, or None if the given file path isn't a string.
        """

        if isinstance(filePath, str):
            return os.path.abspath(filePath)

        return None

    @staticmethod
    def getFileDirectory(filePath: str) -> Union[str, None]:
        """
        Returns the directory path the file is in from the given file path.

        :return: The directory path, or None if a file doesn't exist at the given path.
        """

        if BaseFile.isFile(filePath):
            return os.path.split(filePath)[0]

        return None

    @staticmethod
    def getFileFilename(filePath: str) -> Union[str, None]:
        """
        Returns the name of the file with the extension at the given file path.

        :return: The name of the file, or None if a file doesn't exist at the given path.
        """

        if BaseFile.isFile(filePath):
            return os.path.split(filePath)[1]

        return None

    @staticmethod
    def getFileName(filePath: str) -> Union[str, None]:
        """
        Returns the name of the file without the extension at the given file path.

        :return: The name of the file, or None if a file doesn't exist at the given path.
        """

        if BaseFile.isFile(filePath):
            return os.path.splitext(BaseFile.getFileFilename(filePath))[0]

        return None

    @staticmethod
    def getFileExtension(filePath: str) -> Union[str, None]:
        """
        Returns the extension of the file at the given file path.

        :return: The extension of the file, or None if a file doesn't exist at the given path.
        """

        if BaseFile.isFile(filePath):
            return os.path.splitext(filePath)[1]

        return None

    @staticmethod
    def isFile(filePath: str) -> bool:
        """
        Returns whether or not the given file path is a valid path and a file exists there.

        :return: Whether or not the given file path is a valid path and a file exists there.
        """

        return isinstance(filePath, str) and os.path.isfile(filePath)

    @staticmethod
    def isMode(mode: str) -> bool:
        """
        Returns whether or not the given mode is a valid mode to open a file with. See BaseFile.__MODES.

        :return: Whether or not the given mode is a valid mode to open a file with.
        """

        return isinstance(mode, str) and (mode.lower() in BaseFile.__MODES)