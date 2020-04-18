import json
import datetime
from sqlalchemy import func, extract
from app.models import Account, Applicant


class HRStats(object):
    def __init__(self, username):
        self.hr = Account.find_account(username)

    def pending(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'pending')\
            .filter(Account.id == self.hr.id).count()

    def phone_invite(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'phone_invite')\
            .filter(Account.id == self.hr.id).count()

    def no_reach(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'no_reach')\
            .filter(Account.id == self.hr.id).count()

    def declined(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'declined')\
            .filter(Account.id == self.hr.id).count()

    def interview(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'interview')\
            .filter(Account.id == self.hr.id).count()

    def passed(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'passed')\
            .filter(Account.id == self.hr.id).count()

    def failed(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'failed')\
            .filter(Account.id == self.hr.id).count()

    def hired(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Applicant.status == 'hired')\
            .filter(Account.id == self.hr.id).count()

    def total(self):
        return Account.query.join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Account.id == self.hr.id).count()


class Dashboard(object):
    def __init__(self):
        self.candidate_status = CandidateStatus()
        self.hr_process = HRProcess()
        self.monthly_applicants = MonthlyApplicants()
        self.user_types = UserTypes()

    def total_applicants(self):
        return Applicant.count()

    def total_processed_applicants(self):
        return Applicant.query.filter(Applicant.status != 'pending').count()

    def total_pending_applicants(self):
        return Applicant.query.filter(Applicant.status == 'pending').count()

    def hr_applicant_ratio(self):
        return f'{Account.hr_count()} : {Applicant.count()}'


class CandidateStatus(object):
    def __init__(self):
        pass

    def label_list(self):
        ls = list()
        ls.append('Pending')
        ls.append('Phone Invite')
        ls.append('Can\'t be reached')
        ls.append('Declined')
        ls.append('For interview')
        ls.append('Passed')
        ls.append('Failed')
        ls.append('Hired')
        return ls

    def value_list(self):
        ls = list()
        ls.append(Applicant.query.filter(Applicant.status == 'pending').count())
        ls.append(Applicant.query.filter(Applicant.status == 'phone_invite').count())
        ls.append(Applicant.query.filter(Applicant.status == 'no_reach').count())
        ls.append(Applicant.query.filter(Applicant.status == 'declined').count())
        ls.append(Applicant.query.filter(Applicant.status == 'interview').count())
        ls.append(Applicant.query.filter(Applicant.status == 'passed').count())
        ls.append(Applicant.query.filter(Applicant.status == 'failed').count())
        ls.append(Applicant.query.filter(Applicant.status == 'hired').count())
        return ls

    def color_list(self):
        ls = ['#4e73df', '#8566aa', '#ff5733', '#f6c23e', '#d8ebb5', '#1cc88a', '#e74a3b', '#97e5ef']
        return ls


    def dark_color_list(self):
        ls = ['#2e59d9', '#715196', '#c95238', '#c29932', '#bacc99', '#17a673', '#bf4539', '#8ad2db']
        return ls


class HRProcess(object):
    def __init__(self):
        self.hr_process = dict()

        result = Account.query.add_columns(func.count(Applicant.id))\
            .join(Applicant)\
            .filter(Account.id == Applicant.hr_id)\
            .filter(Account.role == 'hr')\
            .group_by(Account.id).all()

        for r in result:
            hr_name = f'{r[0].first_name} {r[0].last_name}'
            applicant_count = r[1]

            self.hr_process[hr_name] = applicant_count

    def keys(self):
        return list(self.hr_process.keys())

    def values(self):
        return list(self.hr_process.values())


class MonthlyApplicants(object):
    def __init__(self):
        pass

    @classmethod
    def get_applicant_count(cls, month):
        return Applicant.query\
            .filter(extract('month', Applicant.acquire_date) == month)\
            .filter(extract('year', datetime.datetime.now().year))\
            .count()

    def value_list(self):
        ls = list()
        for month in range(1, 12 + 1):
            ls.append(MonthlyApplicants.get_applicant_count(month))
        return ls


class UserTypes(object):
    def __init__(self):
        pass

    @classmethod
    def get_it_percentage(cls):
        count = Account.get_role_count('it')
        total = Account.count()
        return f'{ round(count / total * 100) }%'

    @classmethod
    def get_admin_percentage(cls):
        count = Account.get_role_count('admin')
        total = Account.count()
        return f'{ round(count / total * 100) }%'

    @classmethod
    def get_hr_percentage(cls):
        count = Account.get_role_count('hr')
        total = Account.count()
        return f'{ round(count / total * 100) }%'
