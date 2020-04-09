from datetime import datetime
from lib import choices_from_dict
from app.models import Applicant, CallHistory
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.forms import CalloutForm, PersonalInformation, ScholasticInformation, JobPreference, CallInformation, AdditionalInformation


hr = Blueprint('hr', __name__, url_prefix='/hr')

# =================================== PAGES ===========================================
@hr.route('/dashboard')
@login_required
def home_page():
	# applicants = current_user.applicants
	# return render_template('pages/account/dashboard_hr.html', applicants=applicants)
	return render_template('pages/account/dashboard_hr.html')

@hr.route('/callhistory')
@login_required
def call_history():
	calls = current_user.calls
	return render_template('pages/account/call_history.html', calls=calls)

@hr.route('/process/<applicant_id>')
@login_required
def process_page(applicant_id):
	# Flask Form Here
	form = None
	applicant = Applicant.find_applicant(applicant_id)
	if not applicant:
		flash('Applicant does not exist')
		return redirect(url_for('hr.home_page'))
	return render_template('.html', form=form, applicant=applicant)

@hr.route('/add/applicant')
def add_applicant_page():
	form = CalloutForm(request.form)
	form.personal.marital_status.choices = choices_from_dict(Applicant.MARITAL_STATUS, prepend_blank=False)
	form.education.attainment.choices = choices_from_dict(Applicant.ATTAINMENT, prepend_blank=True)
	form.preference.shift.choices = choices_from_dict(Applicant.SHIFT, prepend_blank=False)
	form.call.disposition.choices = choices_from_dict(Applicant.STATUS, prepend_blank=False)

	return render_template('pages/account/add_applicant.html', form=form)

# ================================ METHODS ==============================================
@hr.route('/doProcess/<applicant_id>', methods=['POST'])
@login_required
def process(applicant_id):
	# Flask Form Here
	applicant = Applicant.find_applicant(applicant_id)
	if form.validate_on_submit():
		applicant.last_name=request.form.get('last_name')
		applicant.first_name=request.form.get('first_name')
		applicant.middle_name=request.form.get('middle_name')
		applicant.birthdate=request.form.get('birthdate')
		applicant.email=request.form.get('email')
		applicant.address=request.form.get('address')
		applicant.mobile1=request.form.get('mobile1')
		applicant.mobile2=request.form.get('mobile2')
		applicant.landline=request.form.get('landline')
		applicant.marital_status=request.form.get('marital_status')
		applicant.educational_attainment=request.form.get('educational_attainment')
		applicant.course=request.form.get('course')
		applicant.graduation_year=request.form.get('graduation_year')
		applicant.applied_position=request.form.get('applied_position')
		applicant.expected_salary=request.form.get('expected_salary')
		applicant.preferred_shift=request.form.get('preferred_shift')
		applicant.preferred_location=request.form.get('preferred_location')
		applicant.status=request.form.get('status')
		applicant.remarks=request.form.get('remarks')
		applicant.source=request.form.get('source')
		applicant.interview_datetime=request.form.get('interview_datetime')
		

		call = CallHistory(
				hr_id=current_user.id,
				applicant_id=applicant.id
			)

		db.session.add(call)
		db.session.commit()
		return redirect(url_for('hr.process_page'))
	
	return render_template('.html', form=form, applicant=applicant)


@hr.route('/add/applicant', methods=['POST'])
@login_required
def add_applicant():
	form = CalloutForm(request.form)

	if form is None:
		return 'Hey'

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

	return redirect(url_for('hr.add_applicant_page'))
