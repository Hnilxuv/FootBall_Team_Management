from flask import request, flash
from werkzeug.security import generate_password_hash
from football_team_manage import db
from football_team_manage.manage.validator import validate_update_data, validate_insert_data
from football_team_manage.models.models import Roles, User


def get_all():
    user_role = Roles.query.filter_by(name='admin').first()
    user_list = User.query.filter_by(role_id=user_role.id).all()
    list = {}
    for item in user_list:
        user = {'id': item.id, 'user_name': item.user_name, 'name': item.name, 'email': item.email,
                'phone': item.phone, 'created_time': item.created_time, 'status': item.status,
                'role_name': item.roles.name}
        list[item.id] = user
    return list


def get(id):
    data = request.form.to_dict()
    role_check = Roles.query.filter_by(name='admin').first()
    user = User.query.filter_by(id=id, role_id=role_check.id).first()
    if user:
        data['username'] = user.user_name
        data['email'] = user.email
        data['name'] = user.name
        data['phone'] = user.phone
        data['role_name'] = user.roles.name
        data['status'] = user.status
        return data
    else:
        return 'not found', 404


def update(id, current_user):
    try:
        data = request.form
        role_check = Roles.query.filter_by(name='admin').first()
        user = User.query.filter_by(id=id, role_id=role_check.id).first()
        user_change = User.query.filter_by(user_name=data['username']).first()
        email_change = User.query.filter_by(email=data['email']).first()
        role = Roles.query.filter_by(name=data['role_name']).first()
        validator = validate_update_data(data)
        if user:
            if user.user_name != current_user.user_name:
                if validator != True:
                    return validator
                else:
                    if data['username'] != user.user_name:
                        if user_change:
                            flash('That username is taken. Please choose a different one.', 'danger')
                            return 'That username is taken. Please choose a different one.'
                    if data['email'] != user.email:
                        if email_change:
                            flash('That email is taken. Please choose a different one.', 'danger')
                            return 'That email is taken. Please choose a different one.'
                    if not role:
                        return 'Invalid role name'
                    else:
                        if data['status'].lower() == 'true':
                            status = True
                        elif data['status'].lower() == 'false':
                            status = False
                        else:
                            return 'invalid status'
                        user.user_name = data['username']
                        user.email = data['email']
                        user.phone = data['phone']
                        user.name = data['name']
                        user.role_id = role.id
                        user.status = status
                        db.session.commit()
                        flash('Update Successfully!', 'success')
                        return 'Update Successfully!'
            else:
                flash('Update unsuccessfully! This account is acting', 'danger')
                return 'Update unsuccessfully! This account is acting'
        else:
            return 'not found', 404
    except:
        flash('Update unsuccessfully!', 'danger')
        return 'Update unsuccessfully!'


def add():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        password_hash = generate_password_hash(password)
        password_confirm = data['confirm_password']
        name = data['name']
        email = data['email']
        phone = data['phone']
        status = True
        role = Roles.query.filter_by(name='admin').first()
        user_name = User.query.filter_by(user_name=username).first()
        user_email = User.query.filter_by(email=email).first()
        validator = validate_insert_data(data)
        if validator != True:
            flash('Add unsuccessfully', 'danger')
            return validator
        elif user_name:
            return 'username is existed'
        elif user_email:
            return 'email is existed'
        elif data['password'] == password_confirm:
            new_user = User(user_name=username, name=name, password=password_hash, email=email, phone=phone,
                            role_id=role.id, status=status)
            db.session.add(new_user)
            db.session.commit()
            flash('Add successfully!', 'success')
            return 'Add successfully'
        else:
            return 'password confirm invalid'
    except:
        flash('Add unsuccessfully', 'danger')
        return 'Add unsuccessfully'


def delete(id, current_user):
    try:
        role_check = Roles.query.filter_by(name='admin').first()
        user = User.query.filter_by(id=id, role_id=role_check.id).first()
        if user:
            if user.user_name != current_user.user_name:
                db.session.delete(user)
                db.session.commit()
                flash('Delete successfully', 'success')
                return 'Delete successfully!'
            else:
                flash('Delete unsuccessfully! This account is acting', 'danger')
                return 'Delete unsuccessfully! This account is acting'
        else:
            return '404 not found', 404
    except:
        flash('Delete unsuccessfully', 'danger')
        return 'Delete unsuccessfully!'
