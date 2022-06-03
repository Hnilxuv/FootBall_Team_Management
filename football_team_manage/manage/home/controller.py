from flask import request, url_for, render_template, redirect
from football_team_manage.manage.form import ChangePasswordForm, UpdateAccountForm
from football_team_manage.manage.home.services import change_account_info, get_account_info, change_password
from football_team_manage.manage.middleware import check_header


def update(current_user):
    if check_header():
        if request.method == 'GET':
            return get_account_info(current_user)
        else:
            return change_account_info(current_user)
    else:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            change_account_info(current_user)
            return redirect(url_for('home.account'))
        if request.method == 'GET':
            data = get_account_info(current_user)
            form = UpdateAccountForm(data=data)
        return render_template('account/account.html', title='Account', form=form, user=current_user)


def change(current_user):
    if check_header():
        return change_password(current_user)
    else:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            change_password(current_user)
            return redirect(url_for('home.change_account_password'))
        return render_template('account/change_password.html', title='Change Password', form=form, user=current_user)
