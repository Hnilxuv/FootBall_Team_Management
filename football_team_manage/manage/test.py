from flask import Blueprint, request, make_response, jsonify
from football_team_manage.manage.auth.controller import register, signin
from football_team_manage.manage.home.controller import get_account_info, change_account_info, change_password
import football_team_manage.manage.manager_user.controller as mu
import football_team_manage.manage.register_user.controller as ru
import football_team_manage.manage.admin_user.controller as au
import football_team_manage.manage.staff_user.controller as su
import football_team_manage.manage.league.controller as ml
import football_team_manage.manage.position.controller as mp
import football_team_manage.manage.player.controller as mpl
import football_team_manage.manage.roles.controller as mr
from football_team_manage.manage.token_required import token_required, has_permission

test = Blueprint('test', __name__)


# @test.errorhandler(400)
# def handle_400_error(_error):
#     return make_response(jsonify({'error': 'not found'}), 400)
#
#
# @test.errorhandler(404)
# def handle_404_error(_error):
#     return make_response(jsonify({'error': 'not found'}), 404)
#
#
# @test.errorhandler(500)
# def handle_500_error(_error):
#     return make_response(jsonify({'error': 'something went wrong'}), 500)
#
#
# @test.errorhandler(405)
# def handle_405_error(_error):
#     return make_response(jsonify({'error': 'invalid method'}), 405)


@test.route('/test/register', methods=['GET', 'POST'])
def signup():
    return register()


@test.route('/test/login', methods=['GET', 'POST'])
def login():
    return signin()


@test.route('/test/account', methods=['GET', 'POST'])
@token_required
def account(current_user):
    if request.method == 'GET':
        return get_account_info(current_user)
    else:
        return change_account_info(current_user)


@test.route('/test/check', methods=['GET', 'POST'])
@token_required
def check(current_user):
    return {'done': current_user.name}


@test.route('/test/changepassword', methods=['GET', 'POST'])
@token_required
def change_account_password(current_user):
    return change_password(current_user)


# manage manager user
@test.route('/test/manager', methods=['GET'])
@token_required
@has_permission(["admin"])
def get_all_manager_user():
    list = mu.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/manager/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_manager_user(id):
    if request.method == 'POST':
        return mu.update(id)
    else:
        return mu.get(id)


@test.route('/test/manager/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_manager_user(id):
    return mu.delete(id)


@test.route('/test/manager/insert', methods=['POST'])
@token_required
@has_permission(["admin"])
def add_manager_user():
    return mu.add()


# manage register user
@test.route('/test/registeruser', methods=['GET'])
@token_required
@has_permission(["admin", "manager"])
def get_all_register_user():
    list = ru.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/registeruser/insert', methods=['POST'])
@token_required
@has_permission(["admin", "manager"])
def add_register_user():
    return ru.add()


@test.route('/test/registeruser/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def update_register_user(current_user, id):
    if request.method == 'GET':
        return ru.get(id)
    else:
        return ru.update(id, current_user)


@test.route('/test/registeruser/delete/<int:id>', methods=['GET', 'POST'])
@token_required
def delete_register_user(current_user, id):
    if current_user.roles.name == 'admin' or current_user.roles.name == 'manager':
        return ru.delete(id)
    else:
        return '404 not found', 404


# manage admin user
@test.route('/test/admin', methods=['GET'])
@token_required
@has_permission(["admin"])
def get_all_admin_user():
    list = au.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/admin/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_admin_user(current_user, id):
    if request.method == 'POST':
        return au.update(id, current_user)
    else:
        return au.get(id)


@test.route('/test/admin/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_admin_user(current_user, id):
    return au.delete(id, current_user)


@test.route('/test/admin/insert', methods=['POST'])
@token_required
@has_permission(["admin"])
def add_admin_user():
    return au.add()


# manage staff user
@test.route('/test/staff', methods=['GET'])
@token_required
@has_permission(["admin", "manager"])
def get_all_staff_user():
    list = su.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/staff/insert', methods=['POST'])
@token_required
@has_permission(["admin", "manager"])
def add_staff_user():
    return su.add()


@test.route('/test/staff/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def update_staff_user(current_user, id):
    if request.method == 'GET':
        return su.get(id)
    else:
        return su.update(id, current_user)


@test.route('/test/staff/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def delete_staff_user(id):
    return su.delete(id)


@test.route('/test/league/insert', methods=['POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def add_league(current_user):
    if current_user.roles.name != 'register user':
        return ml.add()
    else:
        return '404 not found', 404


@test.route('/test/league/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def update_league(current_user, id):
    if current_user.roles.name != 'register user':
        if request.method == 'GET':
            return ml.get(id)
        else:
            return ml.update(id)
    else:
        return '404 not found', 404


@test.route('/test/league', methods=['GET'])
@token_required
@has_permission(["admin", "manager", "staff", "register"])
def get_all_league():
    list = ml.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/league/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def delete_league(current_user, id):
    if current_user.roles.name != 'register user':
        return ml.delete(id)
    else:
        return '404 not found', 404


@test.route('/test/position/insert', methods=['POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def add_position(current_user):
    if current_user.roles.name != 'register user':
        return mp.add()
    else:
        return '404 not found', 404


@test.route('/test/position/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def update_position(id):
    if request.method == 'GET':
        return mp.get(id)
    else:
        return mp.update(id)


@test.route('/test/position', methods=['GET'])
@token_required
@has_permission(["admin", "manager", "staff", "register user"])
def get_all_position():
    list = mp.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/position/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def delete_position(current_user, id):
    if current_user.roles.name != 'register user':
        return mp.delete(id)
    else:
        return '404 not found', 404


@test.route('/test/player/insert', methods=['POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def add_player():
    return mpl.add()


@test.route('/test/player', methods=['GET'])
@token_required
@has_permission(["admin", "manager", "staff", "register user"])
def get_all_player():
    list = mpl.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/player/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def update_player(id):
    if request.method == 'GET':
        return mpl.get(id)
    else:
        return mpl.update(id)


@test.route('/test/player/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager", "staff"])
def delete_player(id):
    return mpl.delete(id)


@test.route('/test/role/insert', methods=['POST'])
@token_required
@has_permission(["admin"])
def add_role():
    return mr.add()


@test.route('/test/role', methods=['GET'])
@token_required
@has_permission(["admin"])
def get_all_roles():
    list = mr.get_all()
    if list:
        return list
    else:
        return 'not found any record'


@test.route('/test/role/update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_roles(id):
    if request.method == 'GET':
        return mr.get(id)
    else:
        return mr.update(id)


@test.route('/test/role/delete/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_roles(id):
    return mr.delete(id)
