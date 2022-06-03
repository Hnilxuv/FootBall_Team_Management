from flask import Blueprint
from football_team_manage.manage.register_user.controller import get_list, insert, update, delete
from football_team_manage.manage.middleware import token_required, has_permission

register_user = Blueprint('register_user', __name__)


@register_user.route('/registeruser')
@token_required
@has_permission(["admin", "manager"])
def get_all_register_user(current_user):
    return get_list(current_user)


@register_user.route('/registeruser/update/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def update_register_user(current_user, id):
    return update(current_user, id)


@register_user.route('/registeruser/delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def delete_manager(current_user, id):
    return delete(id)


@register_user.route('/registeruser/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def add_register_user(current_user):
    return insert(current_user)
