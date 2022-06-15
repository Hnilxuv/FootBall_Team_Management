from football_team_manage.manage.form import UpdateUserForm, InsertionUserForm, EditionUserForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.staff.services as ms
from flask import render_template, url_for, request, redirect


def get_list(current_user):
    page = request.args.get('page', 1, type=int)
    if check_header():
        list = ms.get_all(page)
        if list:
            return list
        else:
            return 'not found any record'
    else:
        list = ms.get_all(page)
        return render_template('staff/staff.html', title='Staff', data=list, user=current_user)


def update(current_user, id):
    if check_header():
        if request.method == 'GET':
            return ms.get(id)
        else:
            return ms.update(id, current_user)
    else:
        if current_user.roles.name == 'manager':
            form = EditionUserForm()
            if form.validate_on_submit():
                ms.update(id, current_user)
                return redirect(url_for('staff.update_staff', id=id))
            if request.method == 'GET':
                data = ms.get(id)
                form = EditionUserForm(data=data)
            return render_template('staff/update_user.html', title='Update Staff', form=form, user=current_user, id=id)
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
            return render_template('staff/update_user.html', title='Update Staff', form=form, user=current_user, id=id)


def insert(current_user):
    if check_header():
        return ms.add()
    else:
        form = InsertionUserForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                ms.add()
                return redirect(url_for('staff.get_all_staff'))
        return render_template('staff/add_user.html', form=form, user=current_user)


def delete(id):
    if check_header():
        return ms.delete(id)
    else:
        ms.delete(id)
        return redirect(url_for('staff.get_all_staff'))
