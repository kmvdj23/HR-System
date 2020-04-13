from datetime import datetime
from collections import OrderedDict
from app.config import db
from flask_login import  UserMixin
from app.models.util import ResourceMixin

class Account(db.Model, ResourceMixin, UserMixin):
    __tablename__ = 'account'

    ROLE = OrderedDict([
        ('it', 'IT'),
        ('admin', 'HR Admin'),
        ('hr', 'HR')
    ])

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    mobile = db.Column(db.String(11), nullable=False)

    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(*ROLE, name='role', native_enum=False),
                    index=True, nullable=False, server_default='it')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    profile_pic = db.Column(db.String(300), nullable=False, default='static/images/default.jpg')

    # Activity tracking for IT
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_date = db.Column(db.DateTime)
    current_sign_in_ip = db.Column(db.String(200))
    last_sign_in_date = db.Column(db.DateTime)
    last_sign_in_ip = db.Column(db.String(200))

    @classmethod
    def find_account(cls, identity):
        return Account.query.filter((cls.username == identity)
            | (cls.email == identity)).first()

    @classmethod
    def get_all_accounts(cls):
        return Account.query.all()

    @classmethod
    def get_all_active_hr(cls):
        return Account.query.filter(cls.role == 'hr' \
            and cls.active == True).all()

    @classmethod
    def count(cls):
        return Account.query.count()

    @classmethod
    def hr_count(cls):
        return Account.query.filter(cls.role == 'hr' \
            and cls.active == True).count()

    def update_activity_tracking(self, ip_address):
        self.sign_in_count = self.sign_in_count + 1
        self.last_sign_in_date = self.current_sign_in_date
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_date = datetime.now()
        self.current_sign_in_ip = ip_address
        self.save()


class Applicant(db.Model, ResourceMixin):
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
    birthdate = db.Column(db.DateTime, nullable=True, default=datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p'))
    email = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=True)
    mobile1 = db.Column(db.String(11), nullable=False, unique=True)
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
    expected_salary = db.Column(db.Integer, nullable=False, default=0)
    preferred_shift = db.Column(db.Enum(*SHIFT, name='preferred_shift', native_enum=False),
                                        index=True, nullable=False, server_default='any')
    preferred_location = db.Column(db.String(50), nullable=True)

    # Call Information
    status = db.Column(db.Enum(*STATUS, name='status', native_enum=False),
                                        index=True, nullable=False, server_default='pending')
    remarks = db.Column(db.String(300), nullable=True)

    # Additional Information
    acquire_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    source = db.Column(db.String(30), nullable=True)
    interview_datetime = db.Column(db.DateTime, nullable=True, default=datetime.strptime('0001-01-01 12:00 AM', '%Y-%m-%d %I:%M %p'))

    # ===================== Relationships ==================================

    hr_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    hr = db.relationship('Account', backref=db.backref('applicants', lazy=True))

    @classmethod
    def find_applicant(cls, id):
        return Applicant.query.filter(cls.id == id).first()

    @classmethod
    def count(cls):
        return Applicant.query.count()


class CallHistory(db.Model, ResourceMixin):

    __tablename__ = 'call_history'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # ======================== RELATIONSHIPS =================================
    hr_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    hr = db.relationship('Account', backref=db.backref('calls', lazy=True))

    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    applicant = db.relationship('Applicant', backref=db.backref('calls', lazy=True))

    @classmethod
    def find_call(cls, id):
        return CallHistory.query.filter(cls.id == id)

    def save(self):
        self.datetime = datetime.now()
        db.session.add(self)
        db.session.commit()
