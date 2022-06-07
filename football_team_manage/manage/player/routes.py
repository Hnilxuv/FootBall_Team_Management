from flask import Blueprint
from football_team_manage.manage.player.controller import get_list, insert, update, delete
from football_team_manage.manage.middleware import token_required, has_permission

player = Blueprint('player', __name__)


@player.route('/player')
@token_required
@has_permission(["admin", "manager", "staff", "register user"])
def get_all_player(current_user):
    return get_list(current_user)


@player.route('/player/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def update_player(current_user, id):
    return update(current_user, id)


@player.route('/player/delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def delete_player(current_user, id):
    return delete(current_user, id)


@player.route('/player/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def add_player(current_user):
    return insert(current_user)



