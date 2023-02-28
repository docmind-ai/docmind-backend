# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, Response
from routes import *
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.

@app.route('/')
def index():
    return 'This is DocMind'

app.register_blueprint(routes)

@app.after_request
def after_request_func(response):
    response.headers["Content-Type"] = 'application/json'
    return response
@app.route('/errors-custom', methods=["GET"])
def customError():
    response = Response(None, 403)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Auth-Token, Origin, Version, Partner-Id, Device-Serial, Device-Uuid, Device-Model, Device-Platform"
    response.headers["Strict-Transport-Security"] = 'max-age=31536000; includeSubDomains; preload'
    return response

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
