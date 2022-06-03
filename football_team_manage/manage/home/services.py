from flask import request, flash
from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_update_account_info, validate_changepw_data
from werkzeug.security import generate_password_hash, check_password_hash
from football_team_manage.models.models import User


def get_account_info(current_user):
    if check_header():
        data = request.get_json()
    else:
        data = request.form.to_dict()
    data['username'] = current_user.user_name
    data['email'] = current_user.email
    data['name'] = current_user.name
    data['phone'] = current_user.phone
    data['role_name'] = current_user.roles.name
    return data


def change_account_info(current_user):
    try:
        if check_header():
            data = request.json
        else:
            data = request.form
        validator = validate_update_account_info(data)
        if validator != True:
            return validator
        else:
            user_change = User.query.filter_by(user_name=data['username']).first()
            email_change = User.query.filter_by(email=data['email']).first()
            if data['username'] != current_user.user_name:
                if user_change:
                    flash('That username is taken. Please choose a different one.', 'danger')
                    return 'That username is taken. Please choose a different one.'
            if data['email'] != current_user.email:
                if email_change:
                    flash('That email is taken. Please choose a different one.', 'danger')
                    return 'That email is taken. Please choose a different one.'
            current_user.user_name = data['username']
            current_user.email = data['email']
            current_user.phone = data['phone']
            current_user.name = data['name']
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return 'Your account has bean update!'
    except:
        flash('Update unsuccessfully!', 'danger')
        return 'update unsuccessfully!'


def change_password(current_user):
    try:
        if check_header():
            data = request.get_json()
        else:
            data = request.form
        validator = validate_changepw_data(data)
        if validator != True:
            return validator
        else:
            if check_password_hash(current_user.password, data['old_password']):
                if data['new_confirm_password'] == data['new_password']:
                    current_user.password = generate_password_hash(data['new_password'])
                    db.session.commit()
                    flash('change password successful!', 'success')
                    return 'change password successful!'
                else:
                    return 'password confirm invalid'
            else:
                flash('invalid old password, please check old password', 'danger')
                return 'invalid old password'
    except:
        flash('change password unsuccessfully!', 'danger')
        return 'change password unsuccessfully!'

