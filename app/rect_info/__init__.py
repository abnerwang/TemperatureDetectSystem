from flask import Blueprint

rect_info = Blueprint('rect_info', __name__)

from . import views
