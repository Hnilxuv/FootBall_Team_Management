from functools import wraps
import jwt
from flask import request, url_for, make_response, redirect
from werkzeug.exceptions import abort

from football_team_manage import app
from football_team_manage.models.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'token' in request.cookies:
            token = request.cookies.get('token')
        if not token:
            return redirect(url_for('auth.login'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            res = make_response(redirect(url_for('auth.login')))
            res.set_cookie("token", value='')
            return res
        return f(current_user, *args, **kwargs)
    return decorator


def has_permission(roles):
    def roles_required(f):
        @wraps(f)
        def decorator(current_user, *args, **kwargs):
            if current_user.roles.name not in roles:
                abort(404)
            return f(current_user, *args, **kwargs)
        return decorator
    return roles_required


def check_header():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        return True
    else:
        return False
