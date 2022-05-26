from flask import request, flash
from football_team_manage import db
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
    data = request.form.to_dict()
    position = Position.query.filter_by(id=id).first()
    if position:
        data['name'] = position.name
        return data
    else:
        return 'not found', 404


def update(id):
    try:
        data = request.form
        position = Position.query.filter_by(id=id).first()
        position_check = Position.query.filter_by(name=data['name']).first()
        validator = validate_data(data)
        if position:
            if validator != True:
                return validator
            else:
                if data['name'] != position.name:
                    if position_check:
                        flash('That name is taken. Please choose a different one.', 'danger')
                        return 'That name is taken. Please choose a different one.'
                    position.name = data['name']
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
            return '404 not found', 404
    except:
        flash('Delete unsuccessfully', 'danger')
        return 'Delete unsuccessfully!'


def add():
    try:
        data = request.json
        name = data['name']
        league_check = Position.query.filter_by(name=data['name']).first()
        validator = validate_data(data)
        if validator != True:
            flash('Add unsuccessfully', 'danger')
            return validator
        elif league_check:
            return 'name is existed'
        else:
            league = Position(name=name)
            db.session.add(league)
            db.session.commit()
            flash('Add successfully!', 'success')
            return 'Add successfully'
    except:
        flash('Add unsuccessfully', 'danger')
        return 'Add unsuccessfully'
