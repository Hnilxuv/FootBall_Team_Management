from flask import request, flash
from werkzeug.exceptions import abort

from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_data
from football_team_manage.models.models import Roles, User


def get_all():
    roles = Roles.query.all()
    list = {}
    for item in roles:
        position = {'id': item.id, 'name': item.name, 'created_time': item.created_time}
        list[item.id] = position
    return list


def get(id):
    if check_header():
        data = request.json
    else:
        data = request.form.to_dict()
    role = Roles.query.filter_by(id=id).first()
    if role:
        if role.name == 'admin':

            return None
        data['name'] = role.name
        return data
    else:
        return abort(404)


def update(id):
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    role = Roles.query.filter_by(id=id).first()
    validator = validate_data(data)
    if role:
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
    else:
        return abort(404)


def delete(id):
    role = Roles.query.filter_by(id=id).first()
    if role:
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
    else:
        return abort(404)


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
