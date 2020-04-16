from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
from app.controllers import main


def it_user(func):
    @wraps(func)
    def is_user():
        if current_user.role == 'it':
            return
        return redirect(url_for('main.error_page'))
    return is_user

def admin_user(func):
    @wraps(func)
    def is_user():
        if current_user.role == 'admin':
            return
        return redirect(url_for('main.error_page'))
    return is_user

def hr_user(func):
    @wraps(func)
    def is_user():
        if current_user.role == 'hr':
            return
        return redirect(url_for('main.error_page'))
    return is_user
