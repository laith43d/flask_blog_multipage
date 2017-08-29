from functools import wraps
from flask import flash, redirect, session, url_for
from models import Users


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Unauthorized access, please login', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def admin_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['username'] is not 'admin':
            flash('Unauthorized access, admin only allowed', 'danger')
            return redirect(url_for('articles'))
        return f(*args, **kwargs)

    return decorated_function

def has_permission(user):
    has_permission = Group.query.filter_by(user = user).get()
    return has_permission

def belongs_to_group(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        return f(*args, **kwargs)

    return decorated_function

