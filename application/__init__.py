from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

import os

if os.environ.get("HEROKU"):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///charactersheets.db"
	app.config["SQLALCHEMY_ECHO"] = True
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# application features
from application import views

from application.characters import models
from application.characters import views

from application.races import models
from application.classes import models
from application.armor import models

from application.weapons import models
from application.weapons import views
#login
from application.auth import models
from application.auth import views

from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

try:
	db.create_all()
except:
	pass