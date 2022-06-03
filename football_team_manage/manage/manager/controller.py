from football_team_manage.manage.form import UpdateUserForm, InsertionUserForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.manager.services as mm
from flask import render_template, url_for, request, redirect


def get_list(current_user):
    if check_header():
        list = mm.get_all()
        if list:
            return list
        else:
            return 'not found any record'
    else:
        dict = mm.get_all()
        list = dict.values()
        return render_template('manager/manager.html', data=list, user=current_user)


def update(current_user, id):
    if check_header():
        if request.method == 'POST':
            return mm.update(id)
        else:
            return mm.get(id)
    else:
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
        return render_template('manager/update_user.html', title='Update Manger User', form=form, user=current_user, id=id)


def insert(current_user):
    if check_header():
        return mm.add()
    else:
        form = InsertionUserForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                mm.add()
                return redirect(url_for('manager.get_all_admin'))
        return render_template('manager/add_user.html', form=form, user=current_user)


def delete(id):
    if check_header():
        return mm.delete(id)
    else:
        mm.delete(id)
        return redirect(url_for('manager.get_all_manager'))