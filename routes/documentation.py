from flask import request, flash
from werkzeug.utils import secure_filename

from . import routes
from helpers.db import connect
import logging
from helpers.utils import checkAuth, build_response
import os
import openai
import re
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'js'}
UPLOAD_FOLDER = '/Users/manojdevender/Documents/GitHub/docmind-backend/uploads'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/uploadFile', methods = ['POST'])
def upload_file():
    conn = connect()
    authRes = checkAuth(conn, request)
    if not authRes['success']:
        return build_response({"status": "error", "message": authRes['message']}, authRes['code'])
    print(authRes)
    # check if the post request has the file part
    if 'file' not in request.files:
        return build_response({"status": "error", "message": "No files found in request"}, 400)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return build_response({"status": "error", "message": "Empty file name found in request"}, 400)
    result = {}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4())
        file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
        sample = open(os.path.join(UPLOAD_FOLDER, unique_filename), "r")
        print(sample.read())
        result['fileId'] = unique_filename
        result['status'] = "success"
        response = build_response(result, 200)
        return response
    return build_response({"status": "error", "message": "Internal Server Error"}, 500)

@routes.route('/documentation/file', methods=["GET"])
def getFileDocumentation():
    conn = connect()
    authRes = checkAuth(conn, request)
    if not authRes['success']:
        return build_response({"status": "error", "message": authRes['message']}, authRes['code'])
    fileId = request.args.get('fileId')
    if not fileId:
        return build_response({"status": "error", "message": "No file found in request"}, 400)
    try:
        sample = open(os.path.join(UPLOAD_FOLDER, fileId), "r")
        fileContent = sample.read()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        result = openai.Completion.create(
              model="text-davinci-003",
              prompt="From the below code , can you list the URL, EndPoint, HttpMethod, QueryParams, Body seperated by commas using equals symbol\n\ncode:\n" + fileContent,
              temperature=0.7,
              max_tokens=256,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )
        extracted_response = {}
        for choice in result['choices']:
            target_string = choice['text']
            target_string = target_string.replace("\n", "")
            target_string = target_string.replace(" ", "")
            word_list = re.split(r",", target_string)
            for word in word_list:
                tokens = word.split('=')
                extracted_response[tokens[0]] = tokens[1]
    except Exception as e:
        logger.error(e)
        response = build_response(
            {"status": "error", "message": "Error getting user details."}, 500)
        return response
    finally:
        conn.close()
    response = build_response(extracted_response, 200)
    return response

@routes.route('/documentation/sample', methods=["GET"])
def getSampleDocumentation():
    conn = connect()
    authRes = checkAuth(conn, request)
    if not authRes['success']:
        return build_response({"status": "error", "message": authRes['message']}, authRes['code'])
    print(authRes)
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        result = openai.Completion.create(
              model="text-davinci-003",
              prompt="From the below typescript code , can you list the URL, EndPoint, HttpMethod, QueryParams, Body seperated by commas using equals symbol\n\ncode:\nlistUserStores(multiBuildings = false) {\n        return this.myHttpService.get(\n            this.AWSEndpoint + `stores?multiBuildings=${multiBuildings}`\n        )\n            .pipe(\n                catchError(MyHttpService.handleErrors)\n            );\n    }",
              temperature=0.7,
              max_tokens=256,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )
        extracted_response = {}
        for choice in result['choices']:
            target_string = choice['text']
            target_string = target_string.replace("\n", "")
            target_string = target_string.replace(" ", "")
            word_list = re.split(r",", target_string)
            for word in word_list:
                tokens = word.split('=')
                extracted_response[tokens[0]] = tokens[1]
    except Exception as e:
        logger.error(e)
        response = build_response(
            {"status": "error", "message": "Error getting user details."}, 500)
        return response
    finally:
        conn.close()
    response = build_response(extracted_response, 200)
    return response
