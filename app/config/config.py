import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager


hr_main = Flask(__name__, template_folder='../views', static_folder='../static')
hr_main.config['SECRET_KEY'] = os.urandom(24)
hr_main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
hr_main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../hr.db'

db = SQLAlchemy(hr_main)
login_manager = LoginManager(hr_main)
login_manager.login_view = 'main.login_page'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(username):
	from app.models import Account
	return Account.query.get(username)