from flask import request, flash
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash
from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_update_data, validate_insert_data
from football_team_manage.models.models import Roles, User


def get_all(page):
    user = User.query.join(Roles).filter(Roles.name == 'staff').order_by(-User.id) \
        .paginate(page=page, per_page=3, error_out=True)
    if check_header():
        list = {}
        for item in user.items:
            user = {'id': item.id, 'user_name': item.user_name, 'name': item.name, 'email': item.email,
                    'phone': item.phone, 'created_time': item.created_time, 'status': item.status,
                    'role_name': item.roles.name}
            list[item.id] = user
        return list
    else:
        return user


def get(id):
    if check_header():
        data = request.json
    else:
        data = request.form.to_dict()
    user = User.query.join(Roles).filter(User.id == id, Roles.name == 'Staff').first_or_404()
    data['username'] = user.user_name
    data['email'] = user.email
    data['name'] = user.name
    data['phone'] = user.phone
    data['role_name'] = user.roles.name
    data['status'] = user.status
    return data


def update(id, current_user):
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    validator = validate_update_data(data)
    user = User.query.join(Roles).filter(User.id == id, Roles.name == 'Staff').first_or_404()
    role = Roles.query.filter_by(name=data['role_name']).first_or_404()
    if validator != True:
        return validator
    else:
        user_change = User.query.filter_by(user_name=data['username']).first()
        email_change = User.query.filter_by(email=data['email']).first()
        if data['username'] != user.user_name:
            if user_change:
                flash('That username is taken. Please choose a different one.', 'danger')
                return 'That username is taken. Please choose a different one.'
        if data['email'] != user.email:
            if email_change:
                flash('That email is taken. Please choose a different one.', 'danger')
                return 'That email is taken. Please choose a different one.'
        else:
            if data['status'].lower() == 'true':
                status = True
            elif data['status'].lower() == 'false':
                status = False
            else:
                return 'invalid status'
            if current_user.roles.name != 'manager':
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
                user.user_name = data['username']
                user.email = data['email']
                user.phone = data['phone']
                user.name = data['name']
                user.status = status
                db.session.commit()
                flash('Update Successfully!', 'success')
                return 'Update Successfully!'


def add():
    try:
        if check_header():
            data = request.json
        else:
            data = request.form
        validator = validate_insert_data(data)
        if validator != True:
            flash('Add unsuccessfully', 'danger')
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
            role = Roles.query.filter_by(name='staff').first_or_404()
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


def delete(id):
    user = User.query.join(Roles).filter(User.id == id, Roles.name == 'Staff').first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('Delete successfully', 'success')
    return 'Delete successfully!', 200
