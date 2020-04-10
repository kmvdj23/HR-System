from app.models import  Account, Applicant
from app.config import db
from flask import redirect, request, session, render_template, url_for, flash, Blueprint

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1' )

@api_v1.route('/getAllApplicants')
def getAllApplicants():
	pass
