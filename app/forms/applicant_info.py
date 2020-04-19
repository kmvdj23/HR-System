# from flask_wtf import FlaskForm
# from wtforms import StringField, DateField, TextAreaField, SelectField
# from wtforms.validators import DataRequired, Optional, Length, Regexp
# from wtforms_components import EmailField, Email
# from lib import choices_from_dict
# from app.models import Applicant


# class PersonalInformation(FlaskForm):
#     last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
#     first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
#     middle_name = StringField('Middle name', validators=[Optional(), Length(max=50)])
#     birthdate = DateField('Date of Birth', validators=[Optional()], format='%Y-%m-%d')
#     landline = StringField('Landline', validators=[Optional(), Length(min=8, max=10), Regexp('^(\d{7,9})|(((\d{2}-)?|\(\d{2}\)?)\d{3}-?\d{4})$', message='Input valid landline number format (e.g. 836-0642, 028360642)')])
#     mobile1 = StringField('Mobile number', validators=[DataRequired(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
#     mobile2 = StringField('Secondary Mobile number', validators=[Optional(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
#     address = TextAreaField('Address', validators=[Optional(), Length(max=300)])
#     email = EmailField('Email', validators=[DataRequired(), Length(max=50), Email()])
#     marital_status = SelectField('Marital status', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.MARITAL_STATUS, prepend_blank=False))


# class ScholasticInformation(FlaskForm):
#     attainment = SelectField('Educational attainment', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.ATTAINMENT, prepend_blank=True))
#     course = StringField('Course', validators=[Optional(), Length(max=30)])
#     graduation_year = StringField('Year Graduated', validators=[Optional(), Length(min=4, max=4), Regexp('^\d{4}$', message='Input valid year format (e.g. 2020)')])


# class JobPreference(FlaskForm):
#     applied_position = StringField('Preferred position', validators=[Optional(), Length(max=50)])
#     expected_salary = StringField('Expected Monthly Salary (in Php)', validators=[Optional(), Length(max=10), Regexp('^\d*$', message='Input valid currency format (e.g. 35000)')])
#     shift = SelectField('Preferred Shift/Schedule', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.SHIFT, prepend_blank=False))
#     location = StringField('Preferred location', validators=[Optional(), Length(max=50)])


# class CallInformation(FlaskForm):
#     disposition = SelectField('Disposition Details', coerce=str, validators=[Optional()], choices=choices_from_dict(Applicant.STATUS, prepend_blank=False))
#     remarks = TextAreaField('Remarks', validators=[Optional(), Length(max=300)])
#     hr = SelectField('HR', coerce=int, validators=[Optional()], choices=[(-1, 'None')])

# class AdditionalInformation(FlaskForm):
#     # acquire_date = DateField('Date Acquired', validators=[Optional()], format='%Y-%m-%d')
#     # callout_date = DateField('Callout Date', validators=[Optional()], format='%Y-%m-%d')
#     # lead = StringField('Lead', validators=[Optional(), Length(max=50)])
#     # source = SelectField('Source', validators=[Optional()], coerce=str, choices=source_list)
#     source = StringField('Source', validators=[Optional(), Length(max=30)])
#     interview_date = DateField('Interview Date', validators=[Optional()], format='%Y-%m-%d')
#     interview_time = StringField('Interview Time', validators=[Optional(), Length(min=3), Regexp('^\d{1,2}(:\d{2})? (am|pm|AM|PM)$', message='Input valid time format (e.g. 9 AM, 08:20 AM)')])
