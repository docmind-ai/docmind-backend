from flask import request
from . import routes
from helpers.db import connect
import logging
from helpers.utils import checkAuth, build_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@routes.route('/documentation', methods=["GET"])
def get():
    conn = connect()
    authRes = checkAuth(conn, request)
    if not authRes['success']:
        return build_response({"status": "error", "message": authRes['message']}, authRes['code'])
    try:
        query = """
            select
                u.id as userId,
                u.username
            from user u
            where u.id = {userId}
        """.format(
            userId=authRes['userId']
        )
        with conn.cursor() as cur:
            cur.execute(query)
            userDetails = cur.fetchone()
    except Exception as e:
        logger.error(e)
        response = build_response(
            {"status": "error", "message": "Error getting user details."}, 500)
        return response
    finally:
        conn.close()
    response = build_response(userDetails, 200)
    return response
