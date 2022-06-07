from flask import Blueprint
from football_team_manage.manage.position.controller import get_list, insert, update, delete
from football_team_manage.manage.middleware import token_required, has_permission

position = Blueprint('position', __name__)


@position.route('/position')
@token_required
@has_permission(["admin", "manager", "staff", "register user"])
def get_all_position(current_user):
    return get_list(current_user)


@position.route('/position/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def update_position(current_user, id):
    return update(current_user, id)


@position.route('/position/delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def delete_position(current_user, id):
    return delete(current_user, id)


@position.route('/position/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def add_position(current_user):
    return insert(current_user)



