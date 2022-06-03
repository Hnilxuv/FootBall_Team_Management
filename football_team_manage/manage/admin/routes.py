from flask import Blueprint
from football_team_manage.manage.admin.controller import get_list, update, insert, delete
from football_team_manage.manage.middleware import token_required, has_permission


admin = Blueprint('admin', __name__)


@admin.route('/admin')
@token_required
@has_permission(["admin"])
def get_all_admin(current_user):
    return get_list(current_user)


@admin.route('/admin/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_admin(current_user, id):
    return update(current_user, id)


@admin.route('/admin/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_admin(current_user, id):
    return delete(current_user, id)


@admin.route('/admin/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def add_admin(current_user):
    return insert(current_user)

