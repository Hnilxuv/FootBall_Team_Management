from flask import request, flash
from werkzeug.exceptions import abort

from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_player_data
from football_team_manage.models.models import Player, Position


def get_all(page):
    players = Player.query.order_by(-Player.id).paginate(page=page, per_page=3)
    if check_header():
        list = {}
        for item in players.items:
            player = {'id': item.id, 'name': item.name, 'shirt_number': item.shirt_number,
                      'age': item.age, 'join_time': item.join_time, 'position_name': item.position.name}
            list[item.id] = player
        return list
    else:
        return players


def get_search(page, search):
    players = Player.query.order_by(-Player.id, Player.name.contains(search)).paginate(page=page, per_page=3)
    if check_header():
        list = {}
        for item in players.items:
            player = {'id': item.id, 'name': item.name, 'shirt_number': item.shirt_number,
                      'age': item.age, 'join_time': item.join_time, 'position_name': item.position.name}
            list[item.id] = player
        return list
    else:
        return players


def get(id):
    if check_header():
        data = request.json
    else:
        data = request.form.to_dict()
    player = Player.query.filter_by(id=id).first_or_404()
    data['name'] = player.name
    data['shirt_number'] = player.shirt_number
    data['age'] = player.age
    data['position_name'] = player.position.name
    return data


def update(id):
    if check_header():
        data = request.json
    else:
        data = request.form
    player = Player.query.filter_by(id=id).first_or_404()
    validator = validate_player_data(data)
    if validator != True:
        return validator
    else:
        shirt_no = Player.query.filter_by(shirt_number=data['shirt_number']).first()
        position = Position.query.filter_by(name=data['position_name']).first_or_404()
        if data['shirt_number'] != player.shirt_number.__str__():
            if shirt_no:
                flash('That shirt number is taken. Please choose a different one!', 'danger')
                return 'That shirt number is taken. Please choose a different one!'
        else:
            player.name = data['name']
            player.age = data['age']
            player.shirt_number = data['shirt_number']
            player.position_id = position.id
            db.session.commit()
            flash('Update successfully!', 'success')
            return 'Update successfully!', 200


def add():
    if check_header():
        data = request.json
    else:
        data = request.form

    validator = validate_player_data(data)
    if validator != True:
        return validator
    else:
        position = Position.query.filter_by(name=data['position_name']).first_or_404()
        name = data['name']
        age = data['age']
        shirt_number = data['shirt_number']
        shirt_no = Player.query.filter_by(shirt_number=data['shirt_number']).first()
        if shirt_no:
            flash('That shirt number is taken. Please choose a different one!', 'danger')
            return 'That shirt number is taken. Please choose a different one!'
        new_player = Player(name=name, shirt_number=shirt_number, age=age, position_id=position.id)
        db.session.add(new_player)
        db.session.commit()
        flash('Add successfully!', 'success')
        return 'Add successfully', 201


def delete(id):
    player = Player.query.filter_by(id=id).first_or_404()
    db.session.delete(player)
    db.session.commit()
    flash('Delete successfully', 'success')
    return 'Delete successfully!', 200
