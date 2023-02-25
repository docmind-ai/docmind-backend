# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from routes import *
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

API_KEY = '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'

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

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
