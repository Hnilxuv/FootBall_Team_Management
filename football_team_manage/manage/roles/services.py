from flask import request, flash
from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_data
from football_team_manage.models.models import Roles, User


def get_all(page):
    roles = Roles.query.order_by(-Roles.id).paginate(page=page, per_page=3)
    if check_header():
        list = {}
        for item in roles.items:
            position = {'id': item.id, 'name': item.name, 'created_time': item.created_time}
            list[item.id] = position
        return list
    else:
        return roles


def get(id):
    if check_header():
        data = request.json
    else:
        data = request.form.to_dict()
    role = Roles.query.filter_by(id=id).first_or_404()
    if role.name == 'admin':
        return None
    data['name'] = role.name
    return data


def update(id):
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    role = Roles.query.filter_by(id=id).first_or_404()
    validator = validate_data(data)
    if validator != True:
        return validator
    else:
        role_check = Roles.query.filter_by(name=data['name']).first()
        if role.name == 'admin':
            flash('That role is not allow to edit. Please choose a different one!', 'danger')
            return 'That role is not allow to edit. Please choose a different one!'
        if data['name'] != role.name:
            if role_check:
                flash('That name is taken. Please choose a different one.', 'danger')
                return 'That name is taken. Please choose a different one.'
        role.name = data['name']
        db.session.commit()
        flash('Update Successfully!', 'success')
        return 'Update Successfully!'


def delete(id):
    role = Roles.query.filter_by(id=id).first_or_404()
    if role.name != 'admin':
        users = User.query.filter_by(role_id=id).all()
        db.session.delete(role)
        for user in users:
            db.session.delete(user)
        db.session.commit()
        flash('Delete successfully', 'success')
        return 'Delete successfully!'
    else:
        flash('That role is not allow to delete. Please choose a different one!', 'danger')
        return 'That role is not allow to delete. Please choose other one!'


def add():
    try:
        if check_header():
            data = request.get_json()
        else:
            data = request.form
        validator = validate_data(data)
        if validator != True:
            flash('Add unsuccessfully', 'danger')
            return validator
        else:
            name = data['name']
            role_check = Roles.query.filter_by(name=data['name']).first()
            if role_check:
                return 'that role name is taken. Please choose a different one!'
            else:
                role = Roles(name=name)
                db.session.add(role)
                db.session.commit()
                flash('Add successfully!', 'success')
                return 'Add successfully',
    except:
        flash('Add unsuccessfully', 'danger')
        return 'Add unsuccessfully'
