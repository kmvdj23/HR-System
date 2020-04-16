from datetime import datetime
from lib import choices_from_dict
from app.models import Applicant, CallHistory
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.forms import CalloutForm, PersonalInformation, ScholasticInformation, JobPreference, CallInformation, AdditionalInformation
from lib.app import hr_user

hr = Blueprint('hr', __name__, url_prefix='/hr')


# =================================== PAGES ===========================================

@hr.route('/dashboard')
@login_required
@hr_user
def home_page():
	applicants = current_user.applicants
	return render_template('pages/account/hr/dashboard.html', applicants=applicants)


@hr.route('/callhistory')
@login_required
@hr_user
def call_history():
	calls = current_user.calls
	return render_template('pages/account/call_history.html', calls=calls)


@hr.route('/<applicant_id>/modify')
@login_required
@hr_user
def edit_applicant_page(applicant_id):
	form = CalloutForm(request.form)
	applicant = Applicant.find_applicant(applicant_id)
	form.personal.address.data = applicant.address
	form.call.remarks.data = applicant.remarks

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	return render_template('pages/account/edit_applicant.html', form=form, applicant=applicant)


@hr.route('/<applicant_id>/call')
@login_required
@hr_user
def call_applicant_page(applicant_id):
	form = CalloutForm(request.form)
	applicant = Applicant.find_applicant(applicant_id)
	form.personal.address.data = applicant.address
	form.call.remarks.data = applicant.remarks

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	return render_template('pages/account/hr/call_applicant.html', form=form, applicant=applicant)


@hr.route('/add/applicant')
@login_required
@hr_user
def add_applicant_page():
	form = CalloutForm(request.form)
	form.personal.marital_status.choices = choices_from_dict(Applicant.MARITAL_STATUS, prepend_blank=False)
	form.education.attainment.choices = choices_from_dict(Applicant.ATTAINMENT, prepend_blank=True)
	form.preference.shift.choices = choices_from_dict(Applicant.SHIFT, prepend_blank=False)
	form.call.disposition.choices = choices_from_dict(Applicant.STATUS, prepend_blank=False)

	return render_template('pages/account/add_applicant.html', form=form)


@hr.route('/<applicant_id>/view')
@login_required
@hr_user
def view_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)
	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	return render_template('pages/account/view_applicant.html', applicant=applicant)


# # ================================ METHODS ==============================================


@hr.route('/<applicant_id>/modify', methods=['POST'])
@login_required
@hr_user
def edit_applicant(applicant_id):
	form = CalloutForm(request.form)
	applicant = Applicant.find_applicant(applicant_id)
	form.personal.address.data = applicant.address
	form.call.remarks.data = applicant.remarks

	if form.validate_on_submit():
		applicant.last_name=request.form.get('personal-last_name')
		applicant.first_name=request.form.get('personal-first_name')
		applicant.middle_name=request.form.get('personal-middle_name')
		applicant.email=request.form.get('personal-email')
		applicant.mobile1=request.form.get('personal-mobile1')
		applicant.mobile2=request.form.get('personal-mobile2')
		applicant.landline=request.form.get('personal-landline')
		applicant.address=request.form.get('personal-address')
		applicant.marital_status=request.form.get('personal-marital_status')
		applicant.course=request.form.get('education-course')
		applicant.graduation_year=request.form.get('education-graduation_year')
		applicant.applied_position=request.form.get('preference-applied_position')
		applicant.expected_salary=request.form.get('preference-expected_salary')
		applicant.preferred_shift=request.form.get('preference-shift')
		applicant.preferred_location=request.form.get('preference-location')
		applicant.status=request.form.get('call-disposition')
		applicant.remarks=request.form.get('call-remarks')
		applicant.source=request.form.get('additional-source')
		applicant.hr_id=current_user.id

		birthdate = request.form.get('personal-birthdate')
		if birthdate != '':
			applicant.birthdate = datetime.strptime('{0}'.format(birthdate), '%Y-%m-%d')

		educational_attainment = request.form.get('education-attainment')
		if educational_attainment != '':
			applicant.educational_attainment = educational_attainment

		interview_date = request.form.get('additional-interview_date')
		interview_time = request.form.get('additional-interview_time')

		if interview_date != '' and interview_time != '':
			timepiece = interview_time.split(" ")

			try:
				hour = timepiece[0].split(":")[0]
				minute = timepiece[0].split(":")[1]
			except IndexError as e:
				minute = '00'

			locale_time = timepiece[1]

			interview_datetime = datetime.strptime('{0} {1}:{2} {3}'.format(interview_date, hour, minute, locale_time), '%Y-%m-%d %I:%M %p')

			applicant.interview_datetime = interview_datetime

		db.session.commit()

		flash('Applicant {0} {1} has been modified'.format(applicant.first_name, applicant.last_name), 'success')
		return redirect(url_for('hr.home_page'))

	else:
		flash('Applicant not modified', 'danger')
		print('==================== ERRORS: add_applicant() ================')
		for err in form.errors:
			print(err)
		print('=============================================================')
		for err in form.personal.errors:
			print(err)
		print('=============================================================')
		for err in form.education.errors:
			print(err)
		print('=============================================================')
		for err in form.preference.errors:
			print(err)
		print('=============================================================')
		for err in form.call.errors:
			print(err)
		print('=============================================================')
		for err in form.additional.errors:
			print(err)

		return render_template('pages/account/edit_applicant.html', form=form, applicant=applicant)

	return redirect(url_for('hr.edit_applicant_page', applicant_id=applicant_id))


@hr.route('/<applicant_id>/call', methods=['POST'])
@login_required
@hr_user
def call_applicant(applicant_id):
	form = CalloutForm(request.form)
	applicant = Applicant.find_applicant(applicant_id)
	form.personal.address.data = applicant.address
	form.call.remarks.data = applicant.remarks

	if form.validate_on_submit():
		applicant.last_name=request.form.get('personal-last_name')
		applicant.first_name=request.form.get('personal-first_name')
		applicant.middle_name=request.form.get('personal-middle_name')
		applicant.email=request.form.get('personal-email')
		applicant.mobile1=request.form.get('personal-mobile1')
		applicant.mobile2=request.form.get('personal-mobile2')
		applicant.landline=request.form.get('personal-landline')
		applicant.address=request.form.get('personal-address')
		applicant.marital_status=request.form.get('personal-marital_status')
		applicant.course=request.form.get('education-course')
		applicant.graduation_year=request.form.get('education-graduation_year')
		applicant.applied_position=request.form.get('preference-applied_position')
		applicant.expected_salary=request.form.get('preference-expected_salary')
		applicant.preferred_shift=request.form.get('preference-shift')
		applicant.preferred_location=request.form.get('preference-location')
		applicant.status=request.form.get('call-disposition')
		applicant.remarks=request.form.get('call-remarks')
		applicant.source=request.form.get('additional-source')
		applicant.hr_id=current_user.id

		birthdate = request.form.get('personal-birthdate')
		if birthdate != '':
			applicant.birthdate = datetime.strptime('{0}'.format(birthdate), '%Y-%m-%d')

		educational_attainment = request.form.get('education-attainment')
		if educational_attainment != '':
			applicant.educational_attainment = educational_attainment

		interview_date = request.form.get('additional-interview_date')
		interview_time = request.form.get('additional-interview_time')

		if interview_date != '' and interview_time != '':
			timepiece = interview_time.split(" ")

			try:
				hour = timepiece[0].split(":")[0]
				minute = timepiece[0].split(":")[1]
			except IndexError as e:
				minute = '00'

			locale_time = timepiece[1]

			interview_datetime = datetime.strptime('{0} {1}:{2} {3}'.format(interview_date, hour, minute, locale_time), '%Y-%m-%d %I:%M %p')

			applicant.interview_datetime = interview_datetime

		call = CallHistory(
			hr_id=current_user.id,
			applicant_id=applicant.id
		)

		db.session.add(call)
		db.session.commit()

		call_date_str = datetime.strftime(call.datetime, '%B %d, %Y %I:%M %p')
		flash('You called applicant {0} {1} on {2}'.format(applicant.first_name, applicant.last_name, call_date_str), 'success')
		return redirect(url_for('hr.home_page'))

	else:
		flash('Applicant not modified', 'danger')
		print('==================== ERRORS: add_applicant() ================')
		for err in form.errors:
			print(err)
		print('=============================================================')
		for err in form.personal.errors:
			print(err)
		print('=============================================================')
		for err in form.education.errors:
			print(err)
		print('=============================================================')
		for err in form.preference.errors:
			print(err)
		print('=============================================================')
		for err in form.call.errors:
			print(err)
		print('=============================================================')
		for err in form.additional.errors:
			print(err)

		return render_template('pages/account/hr/call_applicant.html', form=form, applicant=applicant)

	return redirect(url_for('hr.call_applicant_page', applicant_id=applicant_id))


@hr.route('/add/applicant', methods=['POST'])
@login_required
@hr_user
def add_applicant():
	form = CalloutForm(request.form)

	if form.validate_on_submit():
		applicant = Applicant(
			last_name=request.form.get('personal-last_name'),
			first_name=request.form.get('personal-first_name'),
			middle_name=request.form.get('personal-middle_name'),
			email=request.form.get('personal-email'),
			mobile1=request.form.get('personal-mobile1'),
			mobile2=request.form.get('personal-mobile2'),
			landline=request.form.get('personal-landline'),
			address=request.form.get('personal-address'),
			marital_status=request.form.get('personal-marital_status'),
			course=request.form.get('education-course'),
			graduation_year=request.form.get('education-graduation_year'),
			applied_position=request.form.get('preference-applied_position'),
			expected_salary=request.form.get('preference-expected_salary'),
			preferred_shift=request.form.get('preference-shift'),
			preferred_location=request.form.get('preference-location'),
			status=request.form.get('call-disposition'),
			remarks=request.form.get('call-remarks'),
			source=request.form.get('additional-source'),
			hr_id=current_user.id
		)

		birthdate = request.form.get('personal-birthdate')
		if birthdate != '':
			applicant.birthdate = datetime.strptime('{0}'.format(birthdate), '%Y-%m-%d')

		educational_attainment = request.form.get('education-attainment')
		if educational_attainment != '':
			applicant.educational_attainment = educational_attainment

		interview_date = request.form.get('additional-interview_date')
		interview_time = request.form.get('additional-interview_time')

		if interview_date != '' and interview_time != '':
			timepiece = interview_time.split(" ")

			try:
				hour = timepiece[0].split(":")[0]
				minute = timepiece[0].split(":")[1]
			except IndexError as e:
				minute = '00'

			locale_time = timepiece[1]

			interview_datetime = datetime.strptime('{0} {1}:{2} {3}'.format(interview_date, hour, minute, locale_time), '%Y-%m-%d %I:%M %p')

			applicant.interview_datetime = interview_datetime

		db.session.add(applicant)
		db.session.commit()

		flash('Applicant {0} {1} added successfully'.format(applicant.first_name, applicant.last_name), 'success')
		return redirect(url_for('hr.home_page'))

	else:
		flash('Applicant not created', 'danger')
		print('==================== ERRORS: add_applicant() ================')
		for err in form.errors:
			print(err)
		print('=============================================================')
		for err in form.personal.errors:
			print(err)
		print('=============================================================')
		for err in form.education.errors:
			print(err)
		print('=============================================================')
		for err in form.preference.errors:
			print(err)
		print('=============================================================')
		for err in form.call.errors:
			print(err)
		print('=============================================================')
		for err in form.additional.errors:
			print(err)

		return render_template('pages/account/add_applicant.html', form=form)

	return redirect(url_for('hr.add_applicant_page'))
