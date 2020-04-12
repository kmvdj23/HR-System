import datetime
from collections import OrderedDict
from app.config import db
from flask_login import  UserMixin


class Account(db.Model, UserMixin):

    # TODO: rename fields (e.g. account_type -> role)

    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)

    #Main Fields
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(24), nullable=False)
    account_type = db.Column(db.Integer, nullable=False)

    #Account Details
    first_name = db.Column(db.String(24), nullable=False)
    last_name = db.Column(db.String(24), nullable=False)
    mobile_number = db.Column(db.String(11))
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')


    @classmethod
    def find_account(cls, username):
        return Account.query.filter(cls.username == username).first()

    @classmethod
    def search(cls, query):
        query = '%{0}%'.format(query)
        return Account.query.filter((cls.username == query)
            or (cls.account_type == query)
            or (cls.is_active == query)
            ).all()

    @classmethod
    def get_all_accounts(cls):
        return Account.query.all()

    def is_active(self):
        return self.active

    @classmethod
    def get_callers(cls):
        return Account.query.filter(cls.account_type == 2 and cls.is_active() == True).all()

    @classmethod
    def count(cls):
        return Account.query.count()


class Applicant(db.Model):
    __tablename__ = 'applicant'

    ATTAINMENT = OrderedDict([
        ('none', 'No formal education'),
        ('primary', 'Primary education'),
        ('secondary', 'Secondary education/High school'),
        ('ged', 'General Education Diploma'),
        ('vocational', 'Vocational qualification'),
        ('bachelor\'s', 'Bachelor\'s degree'),
        ('master\'s', 'Master\'s degree'),
        ('doctoral', 'Doctorate or higher')
    ])

    SHIFT = OrderedDict([
        ('any', 'Any'),
        ('day', 'Day Shift'),
        ('mid', 'Mid Shift'),
        ('night', 'Night Shift'),
        ('shift', 'Shifting')
    ])

    MARITAL_STATUS = OrderedDict([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated')
    ])

    STATUS = OrderedDict([
        ('pending', 'Pending'),
        ('phone_invite', 'Phone Invite'),
        ('no_reach', 'Can\'t be reached'),
        ('declined', 'Declined'),
        ('interview', 'For interview'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('hired', 'Hired')
    ])

    id = db.Column(db.Integer, primary_key=True)

    # Personal Information
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    birthdate = db.Column(db.DateTime, nullable=True, default=datetime.datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p'))
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(300), nullable=True)
    mobile1 = db.Column(db.String(11), nullable=False)
    mobile2 = db.Column(db.String(11), nullable=True)
    landline = db.Column(db.String(11), nullable=True)
    marital_status = db.Column(db.Enum(*MARITAL_STATUS, name='marital_status', native_enum=False),
                                index=True, nullable=False, server_default='single')

    # Scholastic Information
    educational_attainment = db.Column(db.Enum(*ATTAINMENT, name='educational_attainment', native_enum=False),
                                        index=True, nullable=False, server_default='bachelor\'s')
    course = db.Column(db.String(30), nullable=True)
    graduation_year = db.Column(db.String(4), nullable=True)

    # Job Preference
    applied_position = db.Column(db.String(50), nullable=True)
    expected_salary = db.Column(db.Integer, nullable=False)
    preferred_shift = db.Column(db.Enum(*SHIFT, name='preferred_shift', native_enum=False),
                                        index=True, nullable=False, server_default='any')
    preferred_location = db.Column(db.String(50), nullable=True)

    # Call Information
    status = db.Column(db.Enum(*STATUS, name='status', native_enum=False),
                                        index=True, nullable=False, server_default='pending')
    remarks = db.Column(db.String(300), nullable=True)

    # Additional Information
    acquire_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    source = db.Column(db.String(30), nullable=True)
    interview_datetime = db.Column(db.DateTime, nullable=True, default=datetime.datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p'))

    # ===================== Relationships ==================================

    hr_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    hr = db.relationship('Account', backref=db.backref('applicants', lazy=True))

    # status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, server_default='1')
    # status = db.relationship('Status', backref=db.backref('applicants', lazy=True))

    @classmethod
    def find_applicant(cls, id):
        return Applicant.query.filter(cls.id == id).first()

    @classmethod
    def search(cls, query):
        query = '%{0}%'.format(query)

        return Applicant.query.filter(
            (cls.first_name == query)
            or (cls.last_name == query)
            or (cls.email == query)
            or (cls.applied_position == query)
            or (cls.expected_salary == query)
            or (cls.source == query)
            or (cls.hr.first_name == query)
            or (cls.hr.last_name == query)
            or (cls.hr.username == query)
            or (cls.status.name == query)
        )

    @classmethod
    def count(cls):
        return Applicant.query.count()


class CallHistory(db.Model):

    __tablename__ = 'call_history'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # ======================== RELATIONSHIPS =================================
    hr_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    hr = db.relationship('Account', backref=db.backref('calls', lazy=True))

    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    applicant = db.relationship('Applicant', backref=db.backref('calls', lazy=True))
    # TODO: create_table, fix html call count

    @classmethod
    def find_call(cls, id):
        return CallHistory.query.filter(cls.id == id)

    @classmethod
    def search(cls, query):
        return Applicant.query.filter(
            (cls.hr_id == query)
            or (cls.applicant_id == query)
            or (cls.datetime == query)
            )
