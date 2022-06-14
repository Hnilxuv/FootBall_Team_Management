from flask import render_template, url_for, request, redirect, flash
from football_team_manage.manage.form import EditionForm, InsertionRolesForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.roles.services as mr


def get_list(current_user):
    page = request.args.get('page', 1, type=int)
    if check_header():
        list = mr.get_all(page)
        if list:
            return list
        else:
            return 'not found any record'
    else:
        list = mr.get_all(page)
        return render_template('roles/role.html', title='Role', data=list, user=current_user)


def update(current_user, id):
    if check_header():
        if request.method == 'GET':
            data = mr.get(id)
            if data:
                return data
            else:
                return 'That role is not allow to edit. Please choose a different one!'
        else:
            return mr.update(id)
    else:
        form = EditionForm()
        if form.validate_on_submit():
            mr.update(id)
            return redirect(url_for('roles.update_role', id=id))
        if request.method == 'GET':
            data = mr.get(id)
            if data:
                form = EditionForm(data=data)
            else:
                flash('That role is not allow to edit. Please choose a different one!', 'danger')
                return redirect(url_for('roles.get_all_role', id=id))
        return render_template('roles/update_role.html', title='Update Role', form=form, user=current_user, id=id)


def delete(current_user, id):
    if check_header():
        return mr.delete(id)
    else:
        mr.delete(id)
        return redirect(url_for('roles.get_all_role'))


def insert(current_user):
    if check_header():
        return mr.add()
    else:
        form = InsertionRolesForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                mr.add()
                return redirect(url_for('roles.get_all_role'))
        return render_template('roles/add_role.html', title='Add Role', form=form, user=current_user)
