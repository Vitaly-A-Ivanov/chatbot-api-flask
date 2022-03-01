import os
from TextAnalysis import chatbot
from TextAnalysis.file.BaseFile import BaseFile



from flask import Flask
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename

# create and configure the app
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "pdf_files"

CORS(app, resources=r"/upload/pdf")


@app.route('/', methods=['GET'])
def run():
    message = request.args.get('message')
    readySubmit = request.args.get('readySubmit')
    topicFound = request.args.get('topicFound')
    fileSubmit = request.args.get('fileSubmit')
    classifiedMsg = request.args.get('classifiedMsg')
    topicSelected = request.args.get('topicSelected')
    topicFinal = request.args.get('topicFinal')
    file = request.args.get('file')
    
    return chatbot.run(message, readySubmit, topicFound, fileSubmit, classifiedMsg, topicSelected, topicFinal, file)


@app.route("/upload/pdf", methods=["GET", "POST"])
def uploadPDF() -> str:
    """
    Saves the uploaded PDF file uploaded via POST.

    If no file was sent, the file is not a PDF, an error occurred, or the request method is not
    POST, an empty string will be returned.

    :return: The file path, or an empty string.
    """

    if request.method == "POST":
        try:
            file = request.files["pdf"]

            # If the file is a PDF
            if file.mimetype == "application/pdf":
                path = toAvailableUploadFilePath(file.filename)
                
                file.save(path)
            
                return path
        except Exception as e:
            print(e)

    return ""


def toUploadFilePath(filename: str) -> str:
    """
    Prepends the upload file path to the filename.

    :return: The updated path.
    """

    return os.path.join(app.config['UPLOAD_FOLDER'],
                        secure_filename(filename))


def toAvailableUploadFilePath(filename: str) -> str:
    """
    Updates the given filename to one that does not exist in the upload folder
    by appending an incrementing number to the filename until a file at that
    location does not exist.

    If a file with the given filename does not initial exist in the upload
    folder, a number won't be appended, returning the path with the original
    filename.
    
    E.g., if a file exists with the name example.txt, it will have an
    incrementing number appended to it, such as:
        example_1.txt
        example_2.txt
        example_3.txt
    until a filename with that name and number does not exist.
    
    :param filename: The name of the file being saved
    :return:         The available file path with the given filename
    """
    
    basename = os.path.splitext(filename)[0]
    path = toUploadFilePath(filename)
    newPath = path
    count = 0

    # Append count to the original filename until a file with the updated name
    # does not exist
    while os.path.isfile(newPath):
        count += 1
        newPath = toUploadFilePath("{}_{}.pdf".format(basename, count))

    return newPath


if __name__ == '__main__':
    app.run()
