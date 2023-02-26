from flask import request
from . import routes
from helpers.db import connect
import logging
from helpers.utils import checkAuth, build_response
import os
import openai
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@routes.route('/documentation', methods=["GET"])
def get():
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
