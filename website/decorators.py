from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from .models import User, Doctor

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user._get_current_object(), User):
            flash('You need to be logged in as a user to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user._get_current_object(), Doctor):
            flash('You need to be logged in as a doctor to access this page.', 'error')
            return redirect(url_for('auth.doctor_login'))
        return f(*args, **kwargs)
    return decorated_function