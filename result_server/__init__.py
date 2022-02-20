from typing import Callable

from flask import Flask, render_template, redirect, url_for, session,flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy, request
from sqlalchemy import exc
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')
app.secret_key = "jefbfjkdbfdb"


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdata.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "getresulton@gmail.com"
app.config['MAIL_PASSWORD'] = "Result@123"
app.config['MAIL_DEFAULT_SENDER'] = "getresulton@gmail.com"


db = MySQLAlchemy(app)

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from result_server import routes