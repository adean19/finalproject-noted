from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

# create the extension
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String, unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    sentiment = db.Column(db.String)
    date_logged = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, user_id, subject, body):
        self.user_id = user_id
        self.subject = subject
        self.body = body