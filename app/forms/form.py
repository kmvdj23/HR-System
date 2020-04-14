from flask_wtf import FlaskForm
from wtforms import FormField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Optional, Length, Regexp, EqualTo
from wtforms_components import EmailField, Email
from wtforms_alchemy import Unique
from app.forms.applicant_info import (
    PersonalInformation,
    ScholasticInformation,
    JobPreference,
    CallInformation,
    AdditionalInformation
)
from app.models import Account
from app.config import db
from lib import choices_from_dict, ModelForm


class AccountForm(ModelForm):
    class Meta:
        model = Account

    first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=30), Unique(Account.username, get_session=lambda: db.session)])
    email = EmailField('Email', validators=[DataRequired(), Length(max=50), Email(), Unique(Account.email, get_session=lambda: db.session)])
    mobile = StringField('Mobile number', validators=[DataRequired(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
    password = PasswordField('Password', validators=[EqualTo('confirm_pass', message='Passwords should match')])
    confirm_pass = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords should match')])
    role = SelectField('Account Type', coerce=str, choices=choices_from_dict(Account.ROLE, prepend_blank=False))
    old_password = PasswordField('Current Password', validators=[EqualTo('confirm_old_pass', message='Passwords should match')])
    confirm_old_pass = PasswordField('Confirm Current Password', validators=[EqualTo('old_password', message='Passwords should match')])


class CalloutForm(FlaskForm):
    personal = FormField(PersonalInformation)
    education = FormField(ScholasticInformation)
    preference = FormField(JobPreference)
    call = FormField(CallInformation)
    additional = FormField(AdditionalInformation)
