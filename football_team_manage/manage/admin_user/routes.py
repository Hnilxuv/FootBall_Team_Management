from flask import Blueprint, render_template, url_for, request, redirect
from football_team_manage.manage.manager_user.form import UpdateUserForm, InsertionForm
from football_team_manage.manage.token_required import token_required, has_permission
import football_team_manage.manage.admin_user.controller as ma


admin = Blueprint('admin', __name__)


@admin.route('/Admin')
@token_required
@has_permission(["admin"])
def get_all_admin(current_user):
    dict = ma.get_all()
    list = dict.values()
    return render_template('admin.html', data=list, user=current_user)


@admin.route('/Admin/Update/<int:id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def update_admin(current_user, id):
    form = UpdateUserForm()
    if form.validate_on_submit():
        ma.update(id, current_user)
        if form.role_name.data != 'admin':
            return redirect(url_for('admin.get_all_admin'))
        else:
            return redirect(url_for('admin.update_admin', id=id))
    if request.method == 'GET':
        data = ma.get(id)
        form = UpdateUserForm(data=data)
    return render_template('update_user.html', title='Update Administrator', form=form, user=current_user, id=id)


@admin.route('/Admin/Delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def delete_admin(current_user, id):
    ma.delete(id, current_user)
    return redirect(url_for('admin.get_all_admin'))


@admin.route('/Admin/Insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin"])
def add_admin(current_user):
    form = InsertionForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            ma.add()
            return redirect(url_for('admin.get_all_admin'))
    return render_template('add_user.html', form=form, user=current_user)
