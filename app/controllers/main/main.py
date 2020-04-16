from lib import password_decrypt, password_encrypt, upload_file
from app.models import Account, Applicant
from app.config import db
from app.forms import AccountForm
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

@main.route('/error')
def error_page():
	return render_template('404.html')

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
		current_user.profile_pic = directory
		db.session.commit()

		return redirect(url_for('main.settings'))
