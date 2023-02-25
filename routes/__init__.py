from flask import Blueprint

routes = Blueprint('routes', __name__)
bp = Blueprint('errors', __name__)

from .user import *


@bp.app_errorhandler(404)
def handle_404(err):
    return build_response({'error': 'Not found'}, 404)


@bp.app_errorhandler(500)
def handle_500(err):
    return build_response({'error': 'Not found'}, 500)
