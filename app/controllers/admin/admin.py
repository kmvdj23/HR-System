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

@admin.rotue('/add/applicant')
@login_required
def add_applicant_page():
	# Flask Form Here
	return render_template('.html', form=form, callers=Account.get_callers())

# ========================= METHODS =======================================

@admin.route('/add/applicant', methods=['POST'])
@login_required
def add_applicant():
	# Flask Form Here

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

		return redirect(url_for('admin.home_page'))

	return render_template('.html', form=form, callers=Account.get_callers())

