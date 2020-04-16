from datetime import datetime
from app.models import Applicant, Account
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from wtforms.validators import DataRequired
from app.forms import ApplicantForm
from lib.app import Dashboard, HRStats
from lib import upload_file
import os

admin = Blueprint('admin', __name__, url_prefix='/admin')


# ========================= PAGES =======================================

@admin.route('/dashboard')
@login_required
def home_page():
	stats = Dashboard()
	return render_template('pages/account/admin/dashboard.html', stats=stats)


@admin.route('/records')
@login_required
def records_page():
	interviewers = Account.get_all_active_hr()
	return render_template('pages/account/admin/records.html', interviewers=interviewers)


@admin.route('/candidates')
@login_required
def candidates_page():
	applicants = Applicant.query.all()
	return render_template('pages/account/admin/candidates.html', applicants=applicants)


@admin.route('/view/hr/<username>')
@login_required
def hr_page(username):
	hr = Account.find_account(username)
	stats = HRStats(hr.username)

	if not hr:
		flash('HR does not exist', 'danger')
		return redirect(url_for('admin.records_page'))

	return render_template('pages/account/admin/profile.html', hr=hr, stats=stats)


@admin.route('/add/applicant')
@login_required
def add_applicant_page():
	form = ApplicantForm()

	form.hr_id.validators.append(DataRequired())
	form.hr_id.choices = list()

	callers = Account.get_all_active_hr()
	for caller in callers:
		form.hr_id.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

	return render_template('pages/account/add_applicant.html', form=form)


@admin.route('/<applicant_id>/modify')
@login_required
def edit_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('admin.candidates_page'))

	form = ApplicantForm(obj=applicant)

	form.hr_id.validators.append(DataRequired())
	form.hr_id.choices = list()
	callers = Account.get_all_active_hr()
	for caller in callers:
		form.hr_id.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

	form.address.data = applicant.address
	form.remarks.data = applicant.remarks

	return render_template('pages/account/edit_applicant.html', form=form, applicant=applicant)


@admin.route('/<applicant_id>/view')
@login_required
def view_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('admin.candidates_page'))

	return render_template('pages/account/view_applicant.html', applicant=applicant)


# ========================= METHODS =======================================

@admin.route('/add/applicant', methods=['POST'])
@login_required
def add_applicant():
	form = ApplicantForm()

	form.hr_id.validators.append(DataRequired())
	form.hr_id.choices = list()

	callers = Account.get_all_active_hr()
	for caller in callers:
		form.hr_id.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

	if form.validate_on_submit():
		applicant = Applicant()
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

		db.session.add(applicant)
		db.session.commit()

		flash(f'Applicant {applicant.first_name} {applicant.last_name} \
			added successfully', 'success')
		return redirect(url_for('admin.candidates_page'))

	else:

		flash('Applicant not created', 'danger')

		print('==================== ERRORS: add_applicant() ================')
		for err in form.errors:
			print(err)

		return render_template('pages/account/add_applicant.html', form=form)

	return redirect(url_for('admin.add_applicant_page'))


@admin.route('/<applicant_id>/modify', methods=['POST'])
@login_required
def edit_applicant(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	form = ApplicantForm(obj=applicant)

	form.hr_id.validators.append(DataRequired())
	form.hr_id.choices = list()
	callers = Account.get_all_active_hr()
	for caller in callers:
		form.hr_id.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

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

		db.session.add(applicant)
		db.session.commit()

		flash(f'Applicant {applicant.first_name} {applicant.last_name} \
			added successfully', 'success')
		return redirect(url_for('admin.candidates_page'))

	else:
		flash('Applicant not modified', 'danger')

		print('==================== ERRORS: edit_applicant() ================')
		for err in form.errors:
			print(err)

		return render_template('pages/account/edit_applicant.html', form=form, applicant=applicant)

	return redirect(url_for('admin.edit_applicant_page', applicant_id=applicant_id))


@admin.route('/import', methods=['POST'])
@login_required
def import_from_csv():
    callers = Account.get_all_active_hr()
    iterator = 0

    if 'csv-input' not in request.files:
        flash('No File Uploaded')
        return redirect(url_for('admin.candidates_page'))

    csv_file = request.files.get('csv-input')

    if csv_file:
        directory = upload_file(csv_file)
        with open(directory, 'r', encoding='utf-8-sig') as file:
            headers = file.readline().strip().split(',')
            line =  file.readline()
            while line:
                data = line.strip().split(',')
                applicant = Applicant(**dict(zip(headers,data)))
                applicant.hr_id = callers[iterator].id
                if iterator == len(callers)-1:
                    iterator = 0
                else:
                    ++iterator
                db.session.add(applicant)

                line = file.readline()
            db.session.commit()
            file.close()

    return redirect(url_for('admin.candidates_page'))
