from flask import Blueprint, render_template
from football_team_manage.manage.home.controller import change, update
from football_team_manage.manage.middleware import token_required

home = Blueprint('home', __name__)


@home.route('/account', methods=['GET', 'POST'])
@token_required
def account(current_user):
    return update(current_user)


@home.route("/changepassword", methods=['GET', 'POST'])
@token_required
def change_account_password(current_user):
    return change(current_user)


@home.route("/")
@home.route("/home")
@token_required
def index(current_user):
    return render_template('home.html', user=current_user)

