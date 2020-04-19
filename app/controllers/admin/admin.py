from datetime import datetime
from app.models import Applicant, Account
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from wtforms.validators import DataRequired
from app.forms import ApplicantForm
from lib.app import Dashboard, HRStats, admin_user
from lib import upload_file
import os

admin = Blueprint('admin', __name__, url_prefix='/admin')


# ========================= PAGES =======================================

@admin.route('/dashboard')
@login_required
@admin_user
def home_page():
	stats = Dashboard()
	return render_template('pages/account/admin/dashboard.html', stats=stats)


@admin.route('/records')
@login_required
@admin_user
def records_page():
	interviewers = Account.get_all_active_hr()
	return render_template('pages/account/admin/records.html', interviewers=interviewers)


@admin.route('/candidates')
@login_required
@admin_user
def candidates_page():
	applicants = Applicant.query.all()
	return render_template('pages/account/admin/candidates.html', applicants=applicants)


@admin.route('/view/hr/<username>')
@login_required
@admin_user
def hr_page(username):
	hr = Account.find_account(username)
	stats = HRStats(hr.username)

	if not hr:
		flash('HR does not exist', 'danger')
		return redirect(url_for('admin.records_page'))

	return render_template('pages/account/admin/profile.html', hr=hr, stats=stats)


@admin.route('/add/applicant')
@login_required
@admin_user
def add_applicant_page():
	return redirect(url_for('main.add_applicant_page'))


@admin.route('/<applicant_id>/modify')
@login_required
@admin_user
def edit_applicant_page(applicant_id):
	return redirect(url_for('main.edit_applicant_page', applicant_id=applicant_id))


@admin.route('/<applicant_id>/view')
@login_required
@admin_user
def view_applicant_page(applicant_id):
	return redirect(url_for('main.view_applicant_page', applicant_id=applicant_id))


# ========================= METHODS =======================================


@admin.route('/import', methods=['POST'])
@login_required
@admin_user
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
