from flask import request, flash
from football_team_manage import db
from football_team_manage.manage.validator import validate_update_data, validate_insert_data, validate_player_data
from football_team_manage.models.models import Player, Position


def get_all():
    players = Player.query.all()
    list = {}
    for item in players:
        player = {'id': item.id, 'name': item.name, 'shirt_number': item.shirt_number,
                  'age': item.age, 'join_time': item.join_time, 'position_name': item.position.name}
        list[item.id] = player
    return list


def get(id):
    data = request.form.to_dict()
    player = Player.query.filter_by(id=id).first()
    if player:
        data['name'] = player.name
        data['shirt_number'] = player.shirt_number
        data['age'] = player.age
        data['join_time'] = player.join_time
        data['position_name'] = player.position.name
        return data
    else:
        return '404 not found', 404


def update(id):
    try:
        data = request.json
        player = Player.query.filter_by(id=id).first()
        shirt_no = Player.query.filter_by(shirt_number=data['shirt_number']).first()
        position = Position.query.filter_by(name=data['position_name']).first()
        validator = validate_player_data(data)
        if player:
            if validator != True:
                return validator
            else:
                if data['shirt_number'] != player.shirt_number:
                    if shirt_no:
                        return 'that shirt number is taken. Please choose a different one!'
                elif not position:
                    return 'invalid position name!'
                else:
                    player.name = data['name']
                    player.age = data['age']
                    player.shirt_number = data['shirt_number']
                    player.position_id = position.id
                    db.session.commit()
                    return 'Update successfully!'
        else:
            return '404 not found', 404
    except:
        return 'Update unsuccessfully!'


def add():
    try:
        data = request.json
        position = Position.query.filter_by(name=data['position_name']).first()
        name = data['name']
        age = data['age']
        shirt_number = data['shirt_number']
        shirt_no = Player.query.filter_by(shirt_number=data['shirt_number']).first()
        validator = validate_player_data(data)
        if validator != True:
            return validator
        elif shirt_no:
            return 'that shirt number is taken. Please choose a different one!'
        elif not position:
            return 'invalid position name'
        new_player = Player(name=name, shirt_number=shirt_number, age=age, position_id=position.id)
        db.session.add(new_player)
        db.session.commit()
        flash('Add successfully!', 'success')
        return 'Add successfully'
    except:
        flash('Add unsuccessfully', 'danger')
        return 'Add unsuccessfully'

def delete(id):
    try:
        player = Player.query.filter_by(id=id).first()
        if player:
            db.session.delete(player)
            db.session.commit()
            flash('Delete successfully', 'success')
            return 'Delete successfully!'
        else:
            return '404 not found', 404
    except:
        flash('Delete unsuccessfully', 'danger')
        return 'Delete unsuccessfully!'
