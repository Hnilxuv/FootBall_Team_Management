from flask import Blueprint
from football_team_manage.manage.manager.controller import delete, get_list, update, insert
from football_team_manage.manage.middleware import token_required, has_permission

manager = Blueprint('manager', __name__)


@manager.route('/manager')
@token_required
@has_permission(["admin"])
def get_all_manager(current_user):
    return get_list(current_user)


@manager.route('/manager/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_manager(current_user, id):
    return update(current_user, id)


@manager.route('/manager/delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_manager(current_user, id):
    return delete(id)


@manager.route('/manager/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def add_manager(current_user):
    return insert(current_user)


