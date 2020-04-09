from flask_wtf import FlaskForm
from wtforms import FormField
from app.forms.applicant_info import (
    PersonalInformation,
    ScholasticInformation,
    JobPreference,
    CallInformation,
    AdditionalInformation
)

class CalloutForm(FlaskForm):
    personal = FormField(PersonalInformation)
    education = FormField(ScholasticInformation)
    preference = FormField(JobPreference)
    call = FormField(CallInformation)
    additional = FormField(AdditionalInformation)
