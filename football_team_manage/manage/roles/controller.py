from flask import request, flash
from football_team_manage import db
from football_team_manage.manage.validator import validate_data
from football_team_manage.models.models import Roles, User


def get_all():
    roles = Roles.query.all()
    list = {}
    for item in roles:
        position = {'id': item.id, 'name': item.name}
        list[item.id] = position
    return list


def get(id):
    data = request.form.to_dict()
    roles = Roles.query.filter_by(id=id).first()
    if roles:
        data['name'] = roles.name
        return data
    else:
        return 'not found', 404


def update(id):
    try:
        data = request.json
        role = Roles.query.filter_by(id=id).first()
        role_check = Roles.query.filter_by(name=data['name']).first()
        validator = validate_data(data)
        if role:
            if validator != True:
                return validator
            else:
                if data['name'] != role.name:
                    if role_check:
                        flash('That name is taken. Please choose a different one.', 'danger')
                        return 'That name is taken. Please choose a different one.'
                    role.name = data['name']
                    db.session.commit()
                    flash('Update Successfully!', 'success')
                    return 'Update Successfully!'
        else:
            return 'not found', 404
    except:
        flash('Update unsuccessfully!', 'danger')
        return 'Update unsuccessfully!'


def delete(id):
    try:
        role = Roles.query.filter_by(id=id).first()
        if role:
            users = User.query.filter_by(role_id=id).all()
            db.session.delete(role)
            for user in users:
                db.session.delete(user)
            db.session.commit()
            flash('Delete successfully', 'success')
            return 'Delete successfully!'
        else:
            return '404 not found', 404
    except:
        flash('Delete unsuccessfully', 'danger')
        return 'Delete unsuccessfully!'


def add():
    try:
        data = request.json
        name = data['name']
        role_check = Roles.query.filter_by(name=data['name']).first()
        validator = validate_data(data)
        if validator != True:
            flash('Add unsuccessfully', 'danger')
            return validator
        elif role_check:
            return 'that role name is taken. Please choose a different one!'
        else:
            role = Roles(name=name)
            db.session.add(role)
            db.session.commit()
            flash('Add successfully!', 'success')
            return 'Add successfully'
    except:
        flash('Add unsuccessfully', 'danger')
        return 'Add unsuccessfully'
