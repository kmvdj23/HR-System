from datetime import datetime
from app.models import Applicant, Account
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from wtforms.validators import DataRequired
from app.forms import CalloutForm, PersonalInformation, ScholasticInformation, JobPreference, CallInformation, AdditionalInformation

admin = Blueprint('admin', __name__, url_prefix='/admin')

# ========================= PAGES =======================================

@admin.route('/dashboard')
@login_required
def home_page():
	#Do Query Here
	return render_template('pages/account/dashboard_admin.html')


@admin.route('/candidates')
@login_required
def candidates_page():
	applicants = Applicant.query.all()
	return render_template('pages/account/admin/candidates.html', applicants=applicants)


@admin.route('/add/applicant')
@login_required
def add_applicant_page():
	form = CalloutForm(request.form)
	form.call.hr.validators.append(DataRequired())
	form.call.hr.choices = list()

	callers = Account.get_callers()
	for caller in callers:
		form.call.hr.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

	return render_template('pages/account/add_applicant.html', form=form)

@admin.route('/<applicant_id>/modify')
@login_required
def edit_applicant_page(applicant_id):
	form = CalloutForm(request.form)
	applicant = Applicant.find_applicant(applicant_id)

	form.call.hr.validators.append(DataRequired())
	form.personal.address.data = applicant.address
	form.call.remarks.data = applicant.remarks
	form.call.hr.choices = list()

	callers = Account.get_callers()
	for caller in callers:
		form.call.hr.choices.append((caller.id, caller.username))

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('admin.candidates_page'))

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
	form = CalloutForm(request.form)
	form.call.hr.validators.append(DataRequired())
	form.call.hr.choices = list()

	callers = Account.get_callers()
	for caller in callers:
		form.call.hr.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

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
			hr_id=request.form.get('call-hr')
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
		# TODO: Make candidate list page
		return redirect(url_for('admin.candidates_page'))

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

	return redirect(url_for('admin.add_applicant_page'))


@admin.route('/<applicant_id>/modify', methods=['POST'])
@login_required
def edit_applicant(applicant_id):
	form = CalloutForm(request.form)
	applicant = Applicant.find_applicant(applicant_id)

	form.call.hr.validators.append(DataRequired())
	form.personal.address.data = applicant.address
	form.call.remarks.data = applicant.remarks
	form.call.hr.choices = list()

	callers = Account.get_callers()
	for caller in callers:
		form.call.hr.choices.append((caller.id, caller.username))

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
		applicant.hr_id=request.form.get('call-hr')

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
		return redirect(url_for('admin.candidates_page'))

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

	return redirect(url_for('admin.edit_applicant_page', applicant_id=applicant_id))


@admin.route('/import', methods=['POST'])
@login_required
def import_from_csv():

    if 'file' not in request.files:
        flash('No File Uploaded')
        return redirect(url_for('admin.candidates_page'))

    csv_file = request.files.get('file')

    if csv_file:
        with open(csv_file, 'r') as file:
            file.readline() #Ignore Column Headers
            line =  file.readline()
            while line:
                details = line.strip().split(',')
                applicant = Applicant(
                    last_name=details[0],
                    first_name=details[1],
                    email=details[2],
                    mobile1=details[3],
                    applied_position=details[4]
                    )

                db.session.add(applicant)

                line = file.readline()
            db.session.commit()
            file.close()

    return redirect(url_for('admin.candidates_page'))
