from flask import Blueprint

upload_image = Blueprint('upload_image', __name__)

from . import views
