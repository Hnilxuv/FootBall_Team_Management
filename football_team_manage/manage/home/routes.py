from flask import Blueprint, request, flash, url_for, render_template, redirect
from football_team_manage import db
from football_team_manage.manage.home.form import ChangePasswordForm, UpdateAccountForm
from football_team_manage.manage.home.controller import change_account_info, get_account_info, change_password
from football_team_manage.manage.token_required import token_required

home = Blueprint('home', __name__)


@home.route('/home/account', methods=['GET', 'POST'])
@token_required
def account(current_user):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        change_account_info(current_user)
        return redirect(url_for('home.account'))
    if request.method == 'GET':
        data = get_account_info(current_user)
        form = UpdateAccountForm(data=data)
    return render_template('account.html', title='Account', form=form, user=current_user)


@home.route("/home/changepassword", methods=['GET','POST'])
@token_required
def change_account_password(current_user):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        change_password(current_user)
        return redirect(url_for('home.change_account_password'))
    return render_template('change_password.html', title='Change Password', form=form, user=current_user)


@home.route("/")
@home.route("/home")
@token_required
def index(current_user):
    return render_template('home.html', user=current_user)
