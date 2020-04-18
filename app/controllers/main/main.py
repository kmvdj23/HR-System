from datetime import datetime
from wtforms.validators import DataRequired
from lib import password_decrypt, password_encrypt, upload_file
from app.models import Account, Applicant
from app.config import db
from app.forms import AccountForm, ApplicantForm
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

main = Blueprint('main', __name__, url_prefix='/main')


#  ========================== PAGES ========================================

@main.route('/')
def login_page():
	if(current_user.is_authenticated and current_user.is_active()):
		return redirect(url_for('main.home_page'))
	else:
		return render_template('index.html')


@main.route('/dashboard')
@login_required
def home_page():
	if current_user.role == 'it':
		return redirect(url_for('it.home_page'))
	elif current_user.role == 'admin':
		return redirect(url_for('admin.home_page'))
	elif current_user.role == 'hr':
		return redirect(url_for('hr.home_page'))


@main.route('/settings')
@login_required
def settings_page():
	form = AccountForm()
	return render_template('pages/settings.html', form=form)


@main.route('/add/applicant')
@login_required
def add_applicant_page():
	form = ApplicantForm()

	if current_user.role == 'admin':
		form.hr_id.validators.append(DataRequired())
		form.hr_id.choices = list()

		callers = Account.get_all_active_hr()
		for caller in callers:
			form.hr_id.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

	return render_template('pages/write_applicant.html', form=form)


@main.route('/<applicant_id>/modify')
@login_required
def edit_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	form = ApplicantForm(obj=applicant)

	if current_user.role == 'admin':
		form.hr_id.validators.append(DataRequired())
		form.hr_id.choices = list()

		callers = Account.get_all_active_hr()
		for caller in callers:
			form.hr_id.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

	form.address.data = applicant.address
	form.remarks.data = applicant.remarks

	return render_template('pages/write_applicant.html', form=form, applicant=applicant)


@main.route('/<applicant_id>/view')
@login_required
def view_applicant_page(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	if not applicant:
		flash('Applicant does not exist', 'danger')
		return redirect(url_for('hr.home_page'))

	return render_template('pages/read_applicant.html', applicant=applicant)


# ============================ METHODS ==============================

@main.route('/login', methods=['POST'])
def login():
	account = Account.find_account(request.form.get('username'))
	if account and password_decrypt(request.form.get('password'), account.password):
		if login_user(account) and account.is_active():
			account.update_activity_tracking(request.remote_addr)
			if account.role == 'it':
				return redirect(url_for('it.home_page'))
			elif account.role == 'admin':
				return redirect(url_for('admin.home_page'))
			elif account.role == 'hr':
				return redirect(url_for('hr.home_page'))
		else:
			flash('That account is disabled', 'danger')
	else:
		flash('Identity or password is incorrect', 'danger')

	return redirect(url_for('main.login_page'))


@login_required
@main.route('/settings', methods=['POST'])
@login_required
def settings():
	form = AccountForm(obj=current_user)

	# Set new labels
	form.password.label.text = 'New password'
	form.confirm_pass.label.text = 'Confirm New Password'

	if form.validate_on_submit():
		current_user.first_name = request.form.get('first_name')
		current_user.last_name = request.form.get('last_name')
		current_user.username = request.form.get('username')
		current_user.mobile = request.form.get('mobile')

		old_pass= request.form.get('old_password')
		new_pass = request.form.get('password')

		if old_pass != '' and new_pass != '' and password_decrypt(old_pass, current_user.password):
			current_user.password = password_encrypt(new_pass)

		db.session.commit()

		flash('Account settings modified', 'success')
		return redirect(url_for('main.settings_page'))

	else:
		flash('Account settings not modified', 'danger')
		return render_template('pages/settings.html', form=form)


@main.route('/logout', methods=['POST'])
@login_required
def logout():
	if request.method == 'POST':
		logout_user()
		return redirect(url_for('main.login_page'))


@main.route('/upload/profile_picture', methods=['POST'])
@login_required
def upload_profile_pic():
	if 'profile-input' in request.files:
		image = request.files.get('profile-input')

		directory = upload_file(image, user=current_user)
		print(directory)

		current_user.profile_pic = directory
		db.session.commit()
		return redirect(url_for('main.settings'))


@main.route('/add/applicant', methods=['POST'])
@login_required
def add_applicant():
	form = ApplicantForm()

	if current_user.role == 'admin':
		form.hr_id.validators.append(DataRequired())
		form.hr_id.choices = list()

		callers = Account.get_all_active_hr()
		for caller in callers:
			form.hr_id.choices.append((caller.id, f'{caller.first_name} {caller.last_name} ({caller.username})'))

	if form.validate_on_submit():
		applicant = Applicant()
		form.populate_obj(applicant)

		if current_user.role == 'hr':
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

		expected_salary = request.form.get('expected_salary')
		if expected_salary != '':
			applicant.expected_salary = int(expected_salary)

		db.session.add(applicant)
		db.session.commit()

		flash(f'Applicant {applicant.first_name} {applicant.last_name} \
			added successfully', 'success')

		if current_user.role == 'admin':
			return redirect(url_for('admin.candidates_page'))
		elif current_user.role == 'hr':
			return redirect(url_for('hr.home_page'))

	else:

		flash('Applicant not created', 'danger')

		print('==================== ERRORS: add_applicant() ================')
		for err in form.errors:
			print(err)

		return render_template('pages/write_applicant.html', form=form)


@main.route('/<applicant_id>/modify', methods=['POST'])
@login_required
def edit_applicant(applicant_id):
	applicant = Applicant.find_applicant(applicant_id)

	form = ApplicantForm(obj=applicant)

	if current_user.role == 'admin':
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

		db.session.commit()

		flash(f'Updated Applicant {applicant.first_name} {applicant.last_name}',
			'success')

		if current_user.role == 'admin':
			return redirect(url_for('admin.candidates_page'))
		elif current_user.role == 'hr':
			return redirect(url_for('hr.home_page'))

	else:
		flash('Applicant not modified', 'danger')

		print('==================== ERRORS: edit_applicant() ================')
		for err in form.errors:
			print(err)

		return render_template('page/write_applicant.html', form=form, applicant=applicant)
