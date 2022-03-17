from flask import Blueprint


faculty_app = Blueprint('faculty_app', __name__, template_folder="templates")


from . import faculty_routes