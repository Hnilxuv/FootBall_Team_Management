import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, request, session
from football_team_manage.manage.middleware import check_header
from football_team_manage.models.models import User, Roles
from datetime import datetime, timedelta
from football_team_manage import app, db
from football_team_manage.manage.validator import validate_register_data, validate_login_data


def register():
    try:
        if check_header():
            data = request.get_json()
        else:
            data = request.form
        validator = validate_register_data(data)
        if validator != True:
            return validator
        else:
            username = data['username']
            password = data['password']
            password_hash = generate_password_hash(password)
            password_confirm = data['confirm_password']
            name = data['name']
            email = data['email']
            phone = data['phone']
            status = True
            role = Roles.query.filter_by(name='register user').first()
            user_name = User.query.filter_by(user_name=username).first()
            user_email = User.query.filter_by(email=email).first()
            if user_name:
                return 'username is existed'
            elif user_email:
                return 'email is existed'
            elif data['password'] == password_confirm:
                new_user = User(user_name=username, name=name, password=password_hash, email=email, phone=phone,
                                role_id=role.id, status=status)
                db.session.add(new_user)
                db.session.commit()
                return 'register successful!'
            else:
                return 'password confirm invalid'
    except:
        return 'register unsuccessful!'


def signin():
    try:
        if check_header():
            data = request.get_json()
        else:
            data = request.form

        validator = validate_login_data(data)
        if validator != True:
            return validator
        else:
            username = data['username']
            password = data['password']
            user_login = User.query.filter_by(user_name=username).first()
            if not user_login:
                flash('Login Unsuccessful. Please check email and password', 'danger')
                return 'Login Unsuccessful. Please check email and password'
            if not check_password_hash(user_login.password, password):
                flash('Login Unsuccessful. Please check email and password', 'danger')
                return 'Login Unsuccessful. Please check email and password'
            if not user_login.status:
                flash('Login Unsuccessful. This account is banned', 'danger')
                return 'Login Unsuccessful. This account is banned'
            token = jwt.encode({'id': user_login.id, 'exp': datetime.utcnow() + timedelta(days=1)},
                               app.config['SECRET_KEY'])
            return token
    except:
        flash('Login Unsuccessful. Please check email and password', 'danger')
        return 'Login Unsuccessful. Please check email and password'




