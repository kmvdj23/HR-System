from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from lib import choices_from_dict

account_type_dict = {
    0: "IT",
    1: "HR Admin",
    2: "HR"
}


class AddUserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    mobile = StringField('Mobile number', validators=[DataRequired(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_pass', message='Passwords should match')])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords should match')])
    account_type = SelectField('Account Type', coerce=int, choices=choices_from_dict(account_type_dict, prepend_blank=False))


class EditUserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    mobile = StringField('Mobile number', validators=[DataRequired(), Length(min=10, max=11), Regexp('^(\d{10,11})|(\d{3,4}-\d{3}-\d{4})$', message='Input valid mobile number format (e.g. 9123456789)')])
    account_type = SelectField('Account Type', coerce=int, choices=choices_from_dict(account_type_dict, prepend_blank=False))
