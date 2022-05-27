from flask import Blueprint, render_template, url_for, request, redirect
from football_team_manage.manage.manager_user.form import UpdateUserForm, InsertionForm
from football_team_manage.manage.token_required import token_required, has_permission
import football_team_manage.manage.manager_user.controller as mm

manager = Blueprint('manager', __name__)


@manager.route('/Manager')
@token_required
@has_permission(["admin"])
def get_all_manager(current_user):
    dict = mm.get_all()
    list = dict.values()
    return render_template('manager.html', data=list, user=current_user)


@manager.route('/Manager/Update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_manager(current_user, id):
    form = UpdateUserForm()
    if form.validate_on_submit():
        mm.update(id)
        if form.role_name.data != 'manager':
            return redirect(url_for('manager.get_all_manager'))
        else:
            return redirect(url_for('manager.update_manager', id=id))
    if request.method == 'GET':
        data = mm.get(id)
        form = UpdateUserForm(data=data)
    return render_template('update_user.html', title='Update Manger User', form=form, user=current_user, id=id)


@manager.route('/Manager/Delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_manager(current_user, id):
    ma.delete(id, current_user)
    return redirect(url_for('manager.get_all_manager'))


@manager.route('/Manager/Insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def add_manager(current_user):
    form = InsertionForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            mm.add()
            return redirect(url_for('manager.get_all_admin'))
    return render_template('add_user.html', form=form, user=current_user)
