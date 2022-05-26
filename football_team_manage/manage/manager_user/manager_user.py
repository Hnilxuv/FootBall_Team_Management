from flask import Blueprint, render_template, url_for, request, redirect, flash
from football_team_manage.manage.manager_user.form import UpdateUserForm, InsertationForm
from football_team_manage.manage.token_required import token_required
import football_team_manage.manage.manager_user.controller as mu

manager = Blueprint('manager', __name__)


@manager.route('/Manager')
@token_required
def get_all_manager(current_user):
    if current_user.roles.name == 'admin':
        dict = mu.get_all()
        if dict:
            list = dict.values()
            return render_template('manager_user.html', data=list, user=current_user)
        else:
            return render_template('notfound.html', user=current_user)
    else:
        return render_template('404.html', user=current_user)


@manager.route('/Manager/Update/<id>', methods=['GET', 'POST'])
@token_required
def update_manager(current_user, id):
    if current_user.roles.name == 'admin':
        form = UpdateUserForm()
        if form.validate_on_submit():
            mu.update(id)
            if form.role_name != 'manager':
                return redirect(url_for('manager.get_all_manager'))
            else:
                return redirect(url_for('manager.update_manager'))
        if request.method == 'GET':
            data = mu.get(id)
            form = UpdateUserForm(data=data)
        return render_template('update_manager.html', title='Update Manger User', form=form, user=current_user, id=id)
    else:
        return render_template('404.html', user=current_user)


@manager.route('/Manager/Delete/<id>', methods=['GET', 'POST'])
@token_required
def delete_manager(current_user, id):
    if current_user.roles.name == 'admin':
        mu.delete(id)
        return redirect(url_for('manager.get_all_manager'))
    else:
        return render_template('404.html', user=current_user)


@manager.route('/Manager/Insert', methods=['GET', 'POST'])
@token_required
def add_manager(current_user):
    if current_user.roles.name == 'admin':
        form = InsertationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                mu.add()
                return redirect(url_for('manager.get_all_manager'))
        return render_template('add_manager.html', form=form, user=current_user)
    else:
        return render_template('404.html', user=current_user)