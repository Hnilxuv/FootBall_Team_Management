from flask import request, flash
from werkzeug.exceptions import abort

from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_data
from football_team_manage.models.models import Position, Player


def get_all():
    positions = Position.query.all()
    list = {}
    for item in positions:
        position = {'id': item.id, 'name': item.name, 'join_time': item.created_time}
        list[item.id] = position
    return list


def get(id):
    if check_header():
        data = request.json
    else:
        data = request.form.to_dict()
    position = Position.query.filter_by(id=id).first()
    if position:
        data['name'] = position.name
        return data
    else:
        return abort(404)


def update(id):
    if check_header():
        data = request.json
    else:
        data = request.form
    position = Position.query.filter_by(id=id).first()

    validator = validate_data(data)
    if position:
        if validator != True:
            return validator
        else:
            position_check = Position.query.filter_by(name=data['name']).first()
            if data['name'] != position.name:
                if position_check:
                    flash('That name is taken. Please choose a different one.', 'danger')
                    return 'That name is taken. Please choose a different one.'
            position.name = data['name']
            db.session.commit()
            flash('Update Successfully!', 'success')
            return 'Update Successfully!'
    else:
        return abort(404)


def delete(id):
    position = Position.query.filter_by(id=id).first()
    if position:
        players = Player.query.filter_by(position_id=id).all()
        db.session.delete(position)
        for player in players:
            db.session.delete(player)
        db.session.commit()
        flash('Delete successfully', 'success')
        return 'Delete successfully!'
    else:
        return abort(404)


def add():
    if check_header():
        data = request.json
    else:
        data = request.form

    validator = validate_data(data)
    if validator != True:
        flash('Add unsuccessfully', 'danger')
        return validator
    else:
        name = data['name']
        position_check = Position.query.filter_by(name=data['name']).first()
        if position_check:
            return 'name is existed'
        else:
            position = Position(name=name)
            db.session.add(position)
            db.session.commit()
            flash('Add successfully!', 'success')
            return 'Add successfully'
