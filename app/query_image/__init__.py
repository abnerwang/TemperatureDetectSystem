from flask import Blueprint

query_image = Blueprint('query_image', __name__)

from . import views