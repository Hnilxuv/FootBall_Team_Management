from flask import request, flash
from werkzeug.exceptions import abort

from football_team_manage import db
from football_team_manage.manage.middleware import check_header
from football_team_manage.manage.validator import validate_data
from football_team_manage.models.models import LeagueJoin


def get_all():
    leagues = LeagueJoin.query.all()
    list = {}
    for item in leagues:
        league = {'id': item.id, 'name': item.name, 'join_time': item.join_time}
        list[item.id] = league
    return list


def get(id):
    if check_header():
        data = request.get_json()
    else:
        data = request.form.to_dict()
    league = LeagueJoin.query.filter_by(id=id).first()
    if league:
        data['name'] = league.name
        return data
    else:
        return abort(404)


def update(id):
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    league = LeagueJoin.query.filter_by(id=id).first()
    validator = validate_data(data)
    if league:
        if validator != True:
            return validator
        else:
            league_check = LeagueJoin.query.filter_by(name=data['name']).first()
            if data['name'] != league.name:
                if league_check:
                    flash('That name is taken. Please choose a different one.', 'danger')
                    return 'That name is taken. Please choose a different one.'
            league.name = data['name']
            db.session.commit()
            flash('Update Successfully!', 'success')
            return 'Update Successfully!'
    else:
        return abort(404)


def delete(id):
    league = LeagueJoin.query.filter_by(id=id).first()
    if league:
        db.session.delete(league)
        db.session.commit()
        flash('Delete successfully', 'success')
        return 'Delete successfully!', 200
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
            league_check = LeagueJoin.query.filter_by(name=data['name']).first()
            if league_check:
                return 'name is existed'
            else:
                league = LeagueJoin(name=name)
                db.session.add(league)
                db.session.commit()
                flash('Add successfully!', 'success')
                return 'Add successfully'
    except:
        flash('Add unsuccessfully', 'danger')
        return 'Add unsuccessfully'
