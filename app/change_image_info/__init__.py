from flask import Blueprint

change_info = Blueprint('change_image_info', __name__)

from . import views
