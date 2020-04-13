from flask_wtf import FlaskForm
from wtforms import FormField, StringField, PasswordField
from wtforms.validators import DataRequired, Optional, Length, Regexp, EqualTo
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


class AccountSettingsForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    mobile = StringField('Mobile number', validators=[DataRequired(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])

    old_pass = PasswordField('Current Password', validators=[Optional(), EqualTo('confirm_old_pass', message='Passwords should match')])
    confirm_old_pass = PasswordField('Confirm current password', validators=[Optional(), EqualTo('old_pass', message='Passwords should match')])

    new_pass = PasswordField('New Password', validators=[Optional(), EqualTo('confirm_new_pass', message='Passwords should match')])
    confirm_new_pass = PasswordField('Confirm new password', validators=[Optional(), EqualTo('new_pass', message='Passwords should match')])
