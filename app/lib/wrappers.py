from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
from app.controllers import main


def it_user(func):
    @wraps(func)
    def is_user(*args, **kwargs):
        if current_user.role == 'it':
            return func(*args, **kwargs)
        return redirect(url_for('main.error_page'))
    return is_user

def admin_user(func):
    @wraps(func)
    def is_user(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        return redirect(url_for('main.error_page'))
    return is_user

def hr_user(func):
    @wraps(func)
    def is_user(*args, **kwargs):
        if current_user.role == 'hr':
            return func(*args, **kwargs)
        return redirect(url_for('main.error_page'))
    return is_user

def human_resource(func):
    @wraps(func)
    def hr(*args, **kwargs):
        if current_user.role in ['hr', 'admin']:
            return func(*args, **kwargs)
        return redirect(url_for('main.error_page'))
    return hr
