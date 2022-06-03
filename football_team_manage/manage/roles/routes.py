from flask import Blueprint
from football_team_manage.manage.roles.controller import update, delete, insert, get_list
from football_team_manage.manage.middleware import token_required, has_permission


roles = Blueprint('roles', __name__)


@roles.route('/role')
@token_required
@has_permission(["admin"])
def get_all_role(current_user):
    return get_list(current_user)


@roles.route('/role/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_role(current_user, id):
    return update(current_user, id)


@roles.route('/role/delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_role(current_user, id):
    return delete(current_user, id)


@roles.route('/role/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def add_role(current_user):
    return insert(current_user)


