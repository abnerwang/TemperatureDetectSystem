from flask import Blueprint

location_manage = Blueprint('location_manage', __name__)

from . import views
