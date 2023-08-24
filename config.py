import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_DEBUG=os.environ.get('FLASK_DEBUG')