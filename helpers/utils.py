from datetime import datetime, date

from flask import Response, json
import logging
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def checkAuth(conn, request):
    token = request.headers.get('X-Auth-Token')
    if token is None:
        return {"message": "No auth token found.", "success": False, "code": 401}
    try:
        with conn.cursor() as cur:
            cur.execute("""
                select
                    u.id as userId
                from authentication_token at
                inner join user u on u.username = at.username
                where at.token = %s
            """, token)
            row = cur.fetchone()
            if row is None:
                conn.close()
                return {"success": False, "message": "Error getting user to check authorisation", "code": 401}
            return {
                "success": True,
                'userId': row['userId'],
            }
    except Exception as e:
        logging.info(e)
        return {"success": False, "message": "Error getting user", "code": 500}


def build_response(resp_dict, status_code):
    response = Response(json.dumps(resp_dict, default=bytesDecodeOverride), status_code)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Strict-Transport-Security"] = 'max-age=31536000; includeSubDomains; preload'
    response.headers["Content-Security-Policy"] = "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'"
    response.headers["X-Content-Type-Options"] = 'nosniff'
    response.headers["X-Frame-Options"] = 'DENY'
    response.headers["X-XSS-Protection"] = '1; mode=block'
    response.headers["Referrer-Policy"] = 'same-origin'
    return response

def bytesDecodeOverride(o):
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, bytes):
        # option 1 - get boolean directly int.from_bytes(o, "big")
        # option 2 - check explicitly if matching boolean values, else fallback to utf
        if o == b'\x00':
            return False
        elif o == b'\x01':
            return True
        else:
            return o.decode('utf-8')
    if isinstance(o, date):
        return str(o)
    if isinstance(o, datetime):
        return str(o)
    return o.decode('utf-8')