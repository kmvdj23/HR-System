from app.models import  Account, Applicant
from app.config import db
from flask import redirect, request, session, render_template, url_for, flash, Blueprint, jsonify

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1' )


# ============================= GET ========================================

@api_v1.route('/getAllApplicants')
def getAllApplicants():
    query = Applicant.query.all()
    applicants = dict()

    for applicant in query:
        applicants[str(applicant.id)] = {
            'id' : applicant.id,
            'last_name' : applicant.last_name,
            'first_name' : applicant.first_name,
            'middle_name' : applicant.middle_name,
            'email' : applicant.email,
            'mobile1' : applicant.mobile1,
            'mobile2' : applicant.mobile2
        }
    return jsonify(applicants)



# ============================ POST =========================================
