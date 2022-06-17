from flask import Blueprint
from football_team_manage.manage.league.controller import insert, delete, update, get_list
from football_team_manage.manage.middleware import token_required, has_permission

league = Blueprint('league', __name__)


@league.route('/league', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff", "register user"])
def get_all_league(current_user):
    return get_list(current_user)


@league.route('/league/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def update_league(current_user, id):
    return update(current_user, id)


@league.route('/league/delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def delete_league(current_user, id):
    return delete(current_user, id)


@league.route('/league/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def add_league(current_user):
    return insert(current_user)


