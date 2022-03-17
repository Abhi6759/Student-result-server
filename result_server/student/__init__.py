from flask import Blueprint


student_app = Blueprint('student_app', __name__, template_folder="templates")

from . import student_routes