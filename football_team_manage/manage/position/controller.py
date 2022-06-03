from flask import render_template, url_for, request, redirect
from football_team_manage.manage.form import EditionForm, InsertionPositionForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.position.services as mp


def get_list(current_user):
    if check_header():
        list = mp.get_all()
        if list:
            return list
        else:
            return 'not found any record'
    else:
        dict = mp.get_all()
        list = dict.values()
        return render_template('position/position.html', title='Position', data=list, user=current_user)


def update(current_user, id):
    if check_header():
        if request.method == 'GET':
            return mp.get(id)
        else:
            return mp.update(id)
    else:
        form = EditionForm()
        if form.validate_on_submit():
            mp.update(id)
            return redirect(url_for('position.update_position', id=id))
        if request.method == 'GET':
            data = mp.get(id)
            form = EditionForm(data=data)
        return render_template('position/update_position.html', title='Update Position', form=form, user=current_user, id=id)


def delete(current_user, id):
    if check_header():
        return mp.delete(id)
    else:
        mp.delete(id)
        return redirect(url_for('position.get_all_position'))


def insert(current_user):
    if check_header():
        return mp.add()
    else:
        form = InsertionPositionForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                mp.add()
                return redirect(url_for('position.get_all_position'))
        return render_template('position/add_position.html', title='Add Position', form=form, user=current_user)
