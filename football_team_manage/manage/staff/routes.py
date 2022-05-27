from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect
import football_team_manage.manage.staff.controller as ms
from football_team_manage.manage.manager_user.form import InsertionForm, UpdateUserForm, UpdateForm
from football_team_manage.manage.token_required import token_required, has_permission

staff = Blueprint('staff', __name__)


@staff.route('/Staff')
@token_required
@has_permission(["admin", "manager"])
def get_all_staff(current_user):
    dict = ms.get_all()
    list = dict.values()
    return render_template('staff.html', data=list, user=current_user)


#
@staff.route('/Staff/Update/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def update_staff(current_user, id):
    if current_user.roles.name == 'manager':
        form = UpdateForm()
        if form.validate_on_submit():
            ms.update(id, current_user)
            return redirect(url_for('staff.update_staff', id=id))
        if request.method == 'GET':
            data = ms.get(id)
            form = UpdateForm(data=data)
        return render_template('update_user.html', title='Update Staff', form=form, user=current_user, id=id)
    else:
        form = UpdateUserForm()
        if form.validate_on_submit():
            ms.update(id, current_user)
            if form.role_name.data != 'staff':
                return redirect(url_for('staff.get_all_staff'))
            else:
                return redirect(url_for('staff.update_staff', id=id))
        if request.method == 'GET':
            data = ms.get(id)
            form = UpdateUserForm(data=data)
        return render_template('update_user.html', title='Update Staff', form=form, user=current_user, id=id)


@staff.route('/Staff/Delete/<id>', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def delete_staff(current_user, id):
    ms.delete(id)
    return redirect(url_for('staff.get_all_staff'))


@staff.route('/Staff/Insert', methods=['GET', 'POST'])
@token_required
@has_permission(["admin", "manager"])
def add_staff(current_user):
    form = InsertionForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            ms.add()
            return redirect(url_for('staff.get_all_staff'))
    return render_template('add_user.html', form=form, user=current_user)
