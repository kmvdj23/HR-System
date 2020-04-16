from flask_wtf import FlaskForm
from wtforms import (
    FormField,
    StringField,
    PasswordField,
    SelectField,
    DateField,
    TextAreaField
)
from wtforms.validators import DataRequired, Optional, Length, Regexp, EqualTo
from wtforms_components import EmailField, Email
from wtforms_alchemy import Unique
from app.models import Account, Applicant
from app.config import db
from lib import choices_from_dict, choices_from_list, ModelForm


class AccountForm(ModelForm):
    class Meta:
        model = Account

    first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=30), Unique(Account.username, get_session=lambda: db.session)])
    email = EmailField('Email', validators=[DataRequired(), Length(max=50), Email(), Unique(Account.email, get_session=lambda: db.session)])
    mobile = StringField('Mobile number', validators=[DataRequired(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
    password = PasswordField('Password', validators=[Optional(), EqualTo('confirm_pass', message='Passwords should match')])
    confirm_pass = PasswordField('Confirm Password', validators=[Optional(), EqualTo('password', message='Passwords should match')])
    role = SelectField('Account Type', coerce=str, choices=choices_from_dict(Account.ROLE, prepend_blank=False))
    old_password = PasswordField('Current Password', validators=[EqualTo('confirm_old_pass', message='Passwords should match')])
    confirm_old_pass = PasswordField('Confirm Current Password', validators=[EqualTo('old_password', message='Passwords should match')])


class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant

    # Personal Information
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle name', validators=[Optional(), Length(max=50)])
    birthdate = DateField('Date of Birth', validators=[Optional()], format='%d/%m/%Y', )
    landline = StringField('Landline', validators=[Optional(), Length(min=8, max=10), Regexp('^(\d{7,9})|(((\d{2}-)?|\(\d{2}\)?)\d{3}-?\d{4})$', message='Input valid landline number format (e.g. 836-0642, 028360642)')])
    mobile1 = StringField('Mobile number', validators=[DataRequired(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
    mobile2 = StringField('Secondary Mobile number', validators=[Optional(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
    address = TextAreaField('Address', validators=[Optional(), Length(max=300)])
    email = EmailField('Email', validators=[DataRequired(), Length(max=50), Email(), Unique(Applicant.email, get_session=lambda: db.session)])
    marital_status = SelectField('Marital status', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.MARITAL_STATUS, prepend_blank=False))

    # Scholastic Information
    educational_attainment = SelectField('Educational attainment', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.ATTAINMENT, prepend_blank=True))
    course = StringField('Course', validators=[Optional(), Length(max=30)])
    graduation_year = StringField('Year Graduated', validators=[Optional(), Length(min=4, max=4), Regexp('^\d{4}$', message='Input valid year format (e.g. 2020)')])

    # Job preference
    applied_position = StringField('Preferred position', validators=[Optional(), Length(max=50)])
    expected_salary = StringField('Expected Monthly Salary (in Php)', validators=[Optional(), Length(max=10), Regexp('^\d*$', message='Input valid currency format (e.g. 35000)')])
    preferred_shift = SelectField('Preferred Shift/Schedule', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.SHIFT, prepend_blank=False))
    preferred_location = StringField('Preferred location', validators=[Optional(), Length(max=50)])

    # Call Information
    status = SelectField('Disposition Details', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.STATUS, prepend_blank=False))
    remarks = TextAreaField('Remarks', validators=[Optional(), Length(max=300)])
    hr_id = SelectField('HR', coerce=int, validators=[Optional()], choices=[(-1, 'None')])

    # Addtional Information
    source = StringField('Source', validators=[Optional(), Length(max=30)])
    interview_date = DateField('Interview Date', validators=[Optional()], format='%d/%m/%Y')
    interview_time = StringField('Interview Time', validators=[Optional(), Length(min=3), Regexp('^\d{1,2}(:\d{2})? (am|pm|AM|PM)$', message='Input valid time format (e.g. 9 AM, 08:20 AM)')])
