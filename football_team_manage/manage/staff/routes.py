from flask import Blueprint
from football_team_manage.manage.staff.controller import insert, delete, get_list, update
from football_team_manage.manage.middleware import token_required, has_permission

staff = Blueprint('staff', __name__)


@staff.route('/staff', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def get_all_staff(current_user):
    return get_list(current_user)


#
@staff.route('/staff/update/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def update_staff(current_user, id):
    return update(current_user, id)


@staff.route('/staff/delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def delete_staff(current_user, id):
    return delete(id)


@staff.route('/staff/insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def add_staff(current_user):
    return insert(current_user)

