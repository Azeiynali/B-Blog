from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../base.db'
# app.config['SECRET_KEY'] = '05111818ea3e3c6ce14b86dff4b95c64c6cafef03dbca3e58f9773652e45ec37'
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
Lomg = LoginManager(app)
Lomg.login_view = 'login'
Lomg.login_message = ''

from blog import routes