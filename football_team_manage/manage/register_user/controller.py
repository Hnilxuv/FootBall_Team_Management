from football_team_manage.manage.form import UpdateUserForm, InsertionUserForm, EditionUserForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.register_user.services as mru
from flask import render_template, url_for, request, redirect


def get_list(current_user):
    page = request.args.get('page', 1, type=int)
    if check_header():
        list = mru.get_all(page)
        if list:
            return list
        else:
            return 'not found any record'
    else:
        list = mru.get_all(page)
        return render_template('register_user/register_user.html',title='Register User', data=list, user=current_user)


def update(current_user, id):
    if check_header():
        if request.method == 'POST':
            return mru.update(id, current_user)
        else:
            return mru.get(id)
    else:
        if current_user.roles.name == 'manager':
            form = EditionUserForm()
            if form.validate_on_submit():
                mru.update(id, current_user)
                return redirect(url_for('register_user.update_register_user', id=id))
            if request.method == 'GET':
                data = mru.get(id)
                form = EditionUserForm(data=data)
            return render_template('register_user/update_user.html', title='Update Register User', form=form, user=current_user,
                                   id=id)
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
            return render_template('register_user/update_user.html', title='Update Register User', form=form, user=current_user, id=id)


def insert(current_user):
    if check_header():
        return mru.add()
    else:
        form = InsertionUserForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                mru.add()
                return redirect(url_for('register_user.get_all_register_user'))
        return render_template('register_user/add_user.html', form=form, user=current_user)


def delete(id):
    if check_header():
        return mru.delete(id)
    else:
        mru.delete(id)
        return redirect(url_for('register_user.get_all_register_user'))