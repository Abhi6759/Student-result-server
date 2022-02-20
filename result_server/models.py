from result_server import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import random

@login_manager.user_loader
def load_user(Faculty_id):
    return Faculty.query.get(int(Faculty_id))

class Students(db.Model):
    seat_no = db.Column(db.Integer, primary_key=True, autoincrement=False, default=None)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    phone_no = db.Column(db.String(20), unique=True, nullable=False)
    english = db.Column(db.Integer, unique=False, nullable=False)
    science = db.Column(db.Integer, unique=False, nullable=False)
    maths = db.Column(db.Integer, unique=False, nullable=False)
    history = db.Column(db.Integer, unique=False, nullable=False)
    IT = db.Column(db.Integer, unique=False, nullable=False)


class Faculty(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=None)
    name = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
