from flask import request, flash
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_update_data, validate_insert_data
from football_team_manage.models.models import Roles, User


def get_all():
    manager_role = Roles.query.filter_by(name='manager').first()
    manager_list = User.query.filter_by(role_id=manager_role.id).all()
    list = {}
    for item in manager_list:
        manager = {'id': item.id, 'user_name': item.user_name, 'name': item.name, 'email': item.email,
                   'phone': item.phone, 'created_time': item.created_time, 'status': item.status,
                   'role_name': item.roles.name}
        list[item.id] = manager
    return list


def get(id):
    if check_header():
        data = request.get_json()
    else:
        data = request.form.to_dict()
    role_check = Roles.query.filter_by(name='manager').first()
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
        return abort(404)


def update(id):
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    role_check = Roles.query.filter_by(name='manager').first()
    user = User.query.filter_by(id=id, role_id=role_check.id).first()
    validator = validate_update_data(data)
    if user:
        if validator != True:
            return validator
        else:
            user_change = User.query.filter_by(user_name=data['username']).first()
            email_change = User.query.filter_by(email=data['email']).first()
            role = Roles.query.filter_by(name=data['role_name']).first()
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
        return abort(404)


def delete(id):
    role_check = Roles.query.filter_by(name='manager').first()
    user = User.query.filter_by(id=id, role_id=role_check.id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Delete successfully', 'success')
        return 'Delete successfully!'
    else:
        abort(404)


def add():
    try:
        if check_header():
            data = request.get_json()
        else:
            data = request.form

        validator = validate_insert_data(data)
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
            role = Roles.query.filter_by(name='manager').first()
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
                flash('Add successfully!', 'success')
                return 'Add successfully'
            else:
                return 'password confirm invalid'
    except:
        flash('Add unsuccessfully', 'danger')
        return 'Add unsuccessfully'
