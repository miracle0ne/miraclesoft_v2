from functools import wraps
from flask import abort
from flask_login import current_user


def admin_requred(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(403)

        if current_user.role.name.lower() != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper