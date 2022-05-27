from flask import Blueprint, make_response, render_template, url_for, redirect, request
from football_team_manage.manage.auth.controller import register, signin
from football_team_manage.models.models import User
from datetime import datetime, timedelta
from football_team_manage import app
import jwt
from football_team_manage.manage.auth.form import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            register()
            user_login = User.query.filter_by(user_name=form.username.data).first()
            token = jwt.encode({'id': user_login.id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                               app.config['SECRET_KEY'])
            res = make_response(redirect(url_for('home.index')))
            res.set_cookie("token", value=token)
            return res
    return render_template('register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        token = signin()
        res = make_response(redirect(url_for('home.index')))
        res.set_cookie("token", value=token)
        return res
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    res = make_response(redirect(url_for('home.index')))
    res.set_cookie("token", value='')
    return res
