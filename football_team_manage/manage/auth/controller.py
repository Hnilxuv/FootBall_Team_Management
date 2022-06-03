from flask import make_response, render_template, url_for, redirect, request
from football_team_manage.manage.auth.services import register, signin
from football_team_manage.manage.middleware import check_header
from football_team_manage.models.models import User
from datetime import datetime, timedelta
from football_team_manage import app
import jwt
from football_team_manage.manage.form import RegistrationForm, LoginForm


def login_auth():
    if check_header():
        return signin()
    else:
        form = LoginForm()
        if form.validate_on_submit():
            token = signin()
            res = make_response(redirect(url_for('home.index')))
            res.set_cookie("token", value=token)
            return res
        return render_template('auth/login.html', title='Login', form=form)


def register_auth():
    if check_header():
        return register()
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                register()
                user_login = User.query.filter_by(user_name=form.username.data).first()
                token = jwt.encode({'id': user_login.id, 'exp': datetime.utcnow() + timedelta(days=1)},
                                   app.config['SECRET_KEY'])
                res = make_response(redirect(url_for('home.index')))
                res.set_cookie("token", value=token)
                return res
        return render_template('auth/register.html', title='Register', form=form)
