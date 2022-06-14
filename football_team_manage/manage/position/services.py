from flask import request, flash
from werkzeug.exceptions import abort

from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_data
from football_team_manage.models.models import Position, Player


def get_all(page):
    positions = Position.query.paginate(page=page, per_page=3)
    if check_header():
        list = {}
        for item in positions.items:
            position = {'id': item.id, 'name': item.name, 'join_time': item.created_time}
            list[item.id] = position
        return list
    else:
        return positions


def get(id):
    if check_header():
        data = request.json
    else:
        data = request.form.to_dict()
    position = Position.query.filter_by(id=id).first_or_404()
    data['name'] = position.name
    return data


def update(id):
    if check_header():
        data = request.json
    else:
        data = request.form
    position = Position.query.filter_by(id=id).first_or_404()
    validator = validate_data(data)
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


def delete(id):
    position = Position.query.filter_by(id=id).first_or_404()
    players = Player.query.filter_by(position_id=id).all()
    db.session.delete(position)
    for player in players:
        db.session.delete(player)
    db.session.commit()
    flash('Delete successfully', 'success')
    return 'Delete successfully!'


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
