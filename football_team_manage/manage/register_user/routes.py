from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect

import football_team_manage.manage.register_user.controller as mru
from football_team_manage.manage.manager_user.form import InsertionForm, UpdateUserForm, UpdateForm
from football_team_manage.manage.test import update_manager_user
from football_team_manage.manage.token_required import token_required, has_permission

register_user = Blueprint('register_user', __name__)


@register_user.route('/RegisterUser')
@token_required
@has_permission(["admin", "manager"])
def get_all_register_user(current_user):
    dict = mru.get_all()
    list = dict.values()
    return render_template('register_user.html', data=list, user=current_user)


#
@register_user.route('/Registeruser/Update/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def update_register_user(current_user, id):
    if current_user.roles.name == 'manager':
        form = UpdateForm()
        if form.validate_on_submit():
            mru.update(id, current_user)
            return redirect(url_for('register_user.update_register_user', id=id))
        if request.method == 'GET':
            data = mru.get(id)
            form = UpdateForm(data=data)
        return render_template('update_user.html', title='Update Register User', form=form, user=current_user, id=id)
    else:
        form = UpdateUserForm()
        if form.validate_on_submit():
            mru.update(id, current_user)
            if form.role_name.data != 'register user':
                return redirect(url_for('register_user.get_all_register_user'))
            else:
                return redirect(url_for('register_user.update_register_user', id=id))
        if request.method == 'GET':
            data = mru.get(id)
            form = UpdateUserForm(data=data)
        return render_template('update_user.html', title='Update Register User', form=form, user=current_user, id=id)


@register_user.route('/Registeruser/Delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def delete_manager(current_user, id):
    mru.delete(id)
    return redirect(url_for('register_user.get_all_register_user'))


@register_user.route('/Registeruser/Insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def add_register_user(current_user):
    form = InsertionForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            mru.add()
            return redirect(url_for('register_user.get_all_register_user'))
    return render_template('add_user.html', form=form, user=current_user)
