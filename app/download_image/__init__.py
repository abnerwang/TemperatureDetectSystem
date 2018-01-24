from flask import Blueprint

download_image = Blueprint('download_image', __name__)

from . import views