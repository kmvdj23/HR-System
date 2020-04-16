from datetime import datetime
from lib import choices_from_dict
from app.models import Applicant, CallHistory
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.forms import ApplicantForm

hr = Blueprint('hr', __name__, url_prefix='/hr')


# =================================== PAGES ===========================================

@hr.route('/dashboard')
@login_required
def home_page():
	applicants = current_user.applicants
	return render_template('pages/account/hr/dashboard.html', applicants=applicants)


@hr.route('/callhistory')
@login_required
def call_history():
	calls = current_user.calls
	return render_template('pages/account/call_history.html', calls=calls)


@hr.route('/<applicant_id>/modify')
@login_required
def edit_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	form = ApplicantForm(obj=applicant)
	form.address.data = applicant.address
	form.remarks.data = applicant.remarks

	return render_template('pages/account/edit_applicant.html', form=form, applicant=applicant)


@hr.route('/<applicant_id>/call')
@login_required
def call_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	form = ApplicantForm(obj=applicant)
	form.address.data = applicant.address
	form.remarks.data = applicant.remarks

	return render_template('pages/account/hr/call_applicant.html', form=form, applicant=applicant)


@hr.route('/add/applicant')
def add_applicant_page():
	form = ApplicantForm()
	return render_template('pages/account/add_applicant.html', form=form)


@hr.route('/<applicant_id>/view')
@login_required
def view_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	return render_template('pages/account/view_applicant.html', applicant=applicant)


# # ================================ METHODS ==============================================


@hr.route('/<applicant_id>/modify', methods=['POST'])
@login_required
def edit_applicant(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)
	form = ApplicantForm(obj=applicant)

	form.address.data = applicant.address
	form.remarks.data = applicant.remarks

	if form.validate_on_submit():
		form.populate_obj(applicant)

		birthdate = request.form.get('birthdate')
		if birthdate != '':
			applicant.birthdate = \
				datetime.strptime(f'{ birthdate }', '%d/%m/%Y')
		else:
			applicant.birthdate = \
				datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

		educational_attainment = request.form.get('educational_attainment')
		if educational_attainment != '' :
			applicant.educational_attainment = educational_attainment
		else:
			applicant.educational_attainment = None

		# TODO: custom validation for this

		interview_date = request.form.get('interview_date')
		interview_time = request.form.get('interview_time')

		if interview_date != '' and interview_time != '':
			time = interview_time.split(' ')

			try:
				hour = time[0].split(':')[0]
				minute = time[0].split(':')[1]
			except IndexError as e:
				minute = '00'

			locale_time = time[1]

			interview_datetime = datetime.strptime(f'{ interview_date } { hour }:{ minute } { locale_time }', '%d/%m/%Y %I:%M %p')
			applicant.interview_datetime = interview_datetime

		db.session.commit()

		flash(f'Applicant {applicant.first_name} {applicant.last_name} \
			added successfully', 'success')

		return redirect(url_for('hr.home_page'))

	else:
		flash('Applicant not modified', 'danger')

		print('==================== ERRORS: edit_applicant() ================')
		for err in form.errors:
			print(err)

		return render_template('pages/account/edit_applicant.html', form=form, applicant=applicant)

	return redirect(url_for('hr.edit_applicant_page', applicant_id=applicant_id))


@hr.route('/<applicant_id>/call', methods=['POST'])
@login_required
def call_applicant(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)
	form = ApplicantForm(obj=applicant)

	form.address.data = applicant.address
	form.remarks.data = applicant.remarks

	if form.validate_on_submit():
		form.populate_obj(applicant)

		birthdate = request.form.get('birthdate')
		if birthdate != '':
			applicant.birthdate = \
				datetime.strptime(f'{ birthdate }', '%d/%m/%Y')
		else:
			applicant.birthdate = \
				datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

		educational_attainment = request.form.get('educational_attainment')
		if educational_attainment != '' :
			applicant.educational_attainment = educational_attainment
		else:
			applicant.educational_attainment = None

		# TODO: custom validation for this

		interview_date = request.form.get('interview_date')
		interview_time = request.form.get('interview_time')

		if interview_date != '' and interview_time != '':
			time = interview_time.split(' ')

			try:
				hour = time[0].split(':')[0]
				minute = time[0].split(':')[1]
			except IndexError as e:
				minute = '00'

			locale_time = time[1]

			interview_datetime = datetime.strptime(f'{ interview_date } { hour }:{ minute } { locale_time }', '%d/%m/%Y %I:%M %p')
			applicant.interview_datetime = interview_datetime

		call = CallHistory(
			hr_id=current_user.id,
			applicant_id=applicant.id
		)

		db.session.add(call)
		db.session.commit()

		call_date_str = datetime.strftime(call.datetime, '%B %d, %Y %I:%M %p')

		flash(f'You called applicant { applicant.first_name } \
			{ applicant.last_name } on { call_date_str }', 'success')

		return redirect(url_for('hr.home_page'))

	else:
		flash('Applicant not modified', 'danger')

		print('==================== ERRORS: call_applicant() ================')
		for err in form.errors:
			print(err)

		return render_template('pages/account/hr/call_applicant.html', form=form, applicant=applicant)

	return redirect(url_for('hr.call_applicant_page', applicant_id=applicant_id))


@hr.route('/add/applicant', methods=['POST'])
@login_required
def add_applicant():
	form = ApplicantForm(request.form)

	if form.validate_on_submit():
		applicant = Applicant()
		form.populate_obj(applicant)
		applicant.hr_id = current_user.id

		birthdate = request.form.get('birthdate')
		if birthdate != '':
			applicant.birthdate = \
				datetime.strptime(f'{ birthdate }', '%d/%m/%Y')
		else:
			applicant.birthdate = \
				datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

		educational_attainment = request.form.get('educational_attainment')
		if educational_attainment != '' :
			applicant.educational_attainment = educational_attainment
		else:
			applicant.educational_attainment = None

		# TODO: custom validation for this

		interview_date = request.form.get('interview_date')
		interview_time = request.form.get('interview_time')

		if interview_date != '' and interview_time != '':
			time = interview_time.split(' ')

			try:
				hour = time[0].split(':')[0]
				minute = time[0].split(':')[1]
			except IndexError as e:
				minute = '00'

			locale_time = time[1]

			interview_datetime = datetime.strptime(f'{ interview_date } { hour }:{ minute } { locale_time }', '%d/%m/%Y %I:%M %p')
			applicant.interview_datetime = interview_datetime

		db.session.add(applicant)
		db.session.commit()

		flash(f'Applicant {applicant.first_name} {applicant.last_name} \
			added successfully', 'success')
		return redirect(url_for('hr.home_page'))

	else:
		flash('Applicant not created', 'danger')

		print('==================== ERRORS: add_applicant() ================')
		for err in form.errors:
			print(err)

		return render_template('pages/account/add_applicant.html', form=form)

	return redirect(url_for('hr.add_applicant_page'))
