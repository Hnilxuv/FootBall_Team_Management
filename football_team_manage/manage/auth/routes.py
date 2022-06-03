from flask import Blueprint, make_response, url_for, redirect
from football_team_manage.manage.auth.controller import login_auth, register_auth

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    return register_auth()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return login_auth()


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    res = make_response(redirect(url_for('home.index')))
    res.set_cookie("token", value='')
    return res
