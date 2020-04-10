from app.models import Applicant, Account
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

# ========================= PAGES =======================================

@admin.route('/dashboard')
@login_required
def home_page():
	#Do Query Here
	return render_template('pages/account/dashboard_admin.html')

@admin.route('/add/applicant')
@login_required
def add_applicant_page():
	# Flask Form Here
	pass
	return render_template('pages/account/add_applicant.html', form=form, callers=Account.get_callers())

# ========================= METHODS =======================================

@admin.route('/add/applicant', methods=['POST'])
@login_required
def add_applicant():
	# Flask Form Here
	pass
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
			applicant.birthdate = birthdate

		educational_attainment = request.form.get('education-attainment')
		if educational_attainment != '':
			applicant.educational_attainment = educational_attainment

		# TODO: Add applicant interview date and time
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

	return redirect(url_for('admin.add_applicant_page'))


@admin.route('/import', methods=['POST'])
@login_required
def import_from_csv():

	if 'file' not in request.files:
		flash('No File Uploaded')
		return redirect(url_for('admin.home_page'))

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

	return redirect(url_for('admin.home_page'))
