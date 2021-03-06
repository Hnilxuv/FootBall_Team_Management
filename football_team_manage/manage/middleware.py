from functools import wraps
import jwt
from flask import request, url_for, make_response, redirect, jsonify
from werkzeug.exceptions import abort

from football_team_manage import app
from football_team_manage.models.models import User


def check_header():
    content_type = request.headers.get('User-Agent')
    if content_type == 'PostmanRuntime/7.29.0':
        return True
    else:
        return False


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if check_header():
            headers = request.headers
            if 'Authorization' in headers:
                bearer = headers.get('Authorization')
                token = bearer.split()[1]
            if not token:
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.query.filter_by(id=data['id']).first()
            except:
                return make_response(jsonify({"message": "Invalid token!"}), 401)
        else:
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



