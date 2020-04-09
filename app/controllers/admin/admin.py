from app.models import Applicant
from app.config import db
from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
def home_page():
	#Do Query Here
	return render_template('pages/account/dashboard_admin.html')