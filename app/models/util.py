from datetime import datetime
from app.config import db


class ResourceMixin(object):
    create_date = db.Column(db.DateTime, default=datetime.now())
    update_date = db.Column(db.DateTime, default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def format_date_to_str(cls, date, format):
        default_datetime = datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

        if date == default_datetime:
            return ''

        return datetime.strftime(date, format)

    @classmethod
    def short_date(cls, date):
        return cls.format_date_to_str(date, '%d/%m/%Y')

    @classmethod
    def long_date(cls, date):
        return cls.format_date_to_str(date, '%B %d, %Y %I:%M %p')

    @classmethod
    def format_time_to_str(cls, date):
        default_datetime = datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

        if date == default_datetime:
            return ''

        return datetime.strftime(date, '%I:%M %p')

