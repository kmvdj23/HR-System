from lib import password_decrypt
from app.models import Account, Applicant
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_user, logout_user, current_user, login_required

main = Blueprint('main', __name__, url_prefix='/main')

#  ========================== PAGES ========================================

@main.route('/')
def login_page():
	if(current_user.is_authenticated):
		return redirect(url_for('main.home_page'))
	else:
		return render_template('index.html')

@main.route('/dashboard')
@login_required
def home_page():
	if current_user.account_type == 0:
		return redirect(url_for('it.home_page'))
	elif current_user.account_type == 1:
		return redirect(url_for('admin.home_page'))
	elif current_user.account_type == 2:
		return redirect(url_for('hr.home_page'))

@login_required
@main.route('/settings')
def settings_page():
	# Flask Form Here
	account = current_user
	return render_template('pages/settings.html', form=form, account=account)

# ============================ METHODS ==============================
@main.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		account = Account.find_account(request.form.get('username'))
		if account and password_decrypt(request.form.get('password'), account.password):
			if login_user(account) and account.account_type == 0:
				return redirect(url_for('it.home_page'))
			elif login_user(account) and account.account_type == 1:
				return redirect(url_for('admin.home_page'))
			elif login_user(account) and account.account_type == 2:
				return redirect(url_for('hr.home_page'))
		else:
			flash('Invalid Account!')
			return redirect(url_for('main.login_page'))
	else:
		flash('Invalid Account!')
		return redirect(url_for('main.login_page'))

@login_required
@main.route('/doSettings', methods=['POST'])
def settings():
	account = current_user
	# Flask Form
	if form.validate_on_submit():
		account.first_name = request.form.get('first_name')
		account.last_name = request.form.get('last_name')
		account.username = request.form.get('username')
		account.password = request.form.get('password')
		account.account_type = request.form.get('account_type')

		db.session.commit()
	return redirect(url_for('main.settings_page'))

@main.route('/logout', methods=['POST'])
@login_required
def logout():
	if request.method == 'POST':
		logout_user()
		return redirect(url_for('main.login_page'))

