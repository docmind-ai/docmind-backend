import os
from dotenv import load_dotenv
import logging
import pymysql.cursors

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# # first, load your env file, replacing the path here with your own if it differs
# # when using the local database make sure you change your path  to .dev.env, it should work smoothly.
# dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
# # update environment just in case
# os.environ.update(dotenv)
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# set globals
RDS_HOST = os.getenv("DB_HOST")
RDS_PORT = int(os.getenv("DB_PORT", 3306))
NAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def connect():
    try:
        cursor = pymysql.cursors.DictCursor
        conn = pymysql.connect(
            host=RDS_HOST, user=NAME, passwd=PASSWORD,
            db=DB_NAME, port=RDS_PORT,
            cursorclass=cursor, connect_timeout=5
        )
        logger.info("SUCCESS: connection to RDS successful")
        return conn
    except Exception as e:
        logging.info(e)
        logger.exception("Database Connection Error")
