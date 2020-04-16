from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import desc

def form_date(value):
	default_datetime = datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p')
	print('====================================================')
	print(value)
	print(type(value))
	if value == default_datetime:
		return ''
	else:
		return datetime.strftime(value, '%Y-%m-%d')


def form_time(value):
	default_datetime = datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p')
	if value == default_datetime:
		return ''
	else:
		return datetime.strftime(value, '%I:%M %p')


def table_date(value):
	default_datetime = datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p')
	if value == default_datetime:
		return ''
	return datetime.strftime(value, '%B %d, %Y %I:%M %p')


def full_name(value):
	from app.models import Applicant
	applicant = Applicant.find_applicant(value)
	if applicant.middle_name != '':
		return f'{applicant.first_name} {applicant.middle_name} {applicant.last_name}'
	else:
		return f'{applicant.first_name} {applicant.last_name}'


def no_scholastic_info(value):
	from app.models import Applicant
	applicant = Applicant.find_applicant(value)
	return (not applicant.educational_attainment and not applicant.course and not applicant.graduation_year)


def no_preference(value):
	from app.models import Applicant
	applicant = Applicant.find_applicant(value)
	return (not applicant.applied_position and not applicant.expected_salary and not applicant.preferred_shift and not applicant.preferred_location)

def no_call_info(value):
	from app.models import Applicant
	applicant = Applicant.find_applicant(value)
	return (not applicant.status and not applicant.remarks)


def no_additional_info(value):
	default_datetime = datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p')
	from app.models import Applicant
	applicant = Applicant.find_applicant(value)
	return(not applicant.source and applicant.interview_datetime == default_datetime)


def select(value):
	from app.models import Applicant
	values = dict()
	values.update(Applicant.ATTAINMENT)
	values.update(Applicant.SHIFT)
	values.update(Applicant.MARITAL_STATUS)
	values.update(Applicant.STATUS)
	return values[value]


def last_call_date(value):
	from app.models import Applicant, CallHistory
	callHistory = CallHistory.query.join(Applicant)\
		.filter(CallHistory.applicant_id == Applicant.id)\
		.order_by(desc(CallHistory.datetime))\
		.filter(Applicant.id == value).first()

	if not callHistory:
		return ''
	else:
		return callHistory.datetime



hr_main = Flask(__name__, template_folder='../views', static_folder='../static')
hr_main.config['SECRET_KEY'] = os.urandom(24)
hr_main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
hr_main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../hr.db'

# jinja filters
hr_main.jinja_env.filters['form_date'] = form_date
hr_main.jinja_env.filters['form_time'] = form_time
hr_main.jinja_env.filters['table_date'] = table_date
hr_main.jinja_env.filters['full_name'] = full_name
hr_main.jinja_env.filters['no_scholastic_info'] = no_scholastic_info
hr_main.jinja_env.filters['no_preference'] = no_preference
hr_main.jinja_env.filters['no_call_info'] = no_call_info
hr_main.jinja_env.filters['no_additional_info'] = no_additional_info
hr_main.jinja_env.filters['select'] = select
hr_main.jinja_env.filters['last_call_date'] = last_call_date


db = SQLAlchemy(hr_main)
login_manager = LoginManager(hr_main)
login_manager.login_view = 'main.login_page'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(username):
	from app.models import Account
	return Account.query.get(username)


@hr_main.context_processor
def inject_now():
	return { 'now': datetime.now() }
