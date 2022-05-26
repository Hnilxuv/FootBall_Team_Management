from flask import Blueprint, render_template
import football_team_manage.manage.register_user.controller as ru
from football_team_manage.manage.token_required import token_required

register_user = Blueprint('register_user', __name__)


@register_user.route('/RegisterUser')
@token_required
def get_all_register_user(current_user):
    if current_user.roles.name == 'admin' or current_user.roles.name == 'manager':
        dict = ru.get_all()
        if dict:
            list = dict.values()
            return render_template('register_user.html', data=list, user=current_user)
        else:
            return render_template('notfound.html', user=current_user)
    else:
        return render_template('404.html', user=current_user)

#
# @manager.route('/Manager/Update/<id>', methods=['GET', 'POST'])
# @token_required
# def update_manager(current_user, id):
#     if current_user.roles.name == 'admin':
#         form = UpdateUserForm()
#         if form.validate_on_submit():
#             update_manager_user(id)
#             return redirect(url_for('manager.update_manager', id=id))
#         if request.method == 'GET':
#             data = get_manager_user(id)
#             form = UpdateUserForm(data=data)
#         return render_template('update_manager.html', title='Update Manger User', form=form, user=current_user, id=id)
#     else:
#         return render_template('404.html', user=current_user)
#
#
# @manager.route('/Manager/Delete/<id>', methods=['GET', 'POST'])
# @token_required
# def delete_manager(current_user, id):
#     if current_user.roles.name == 'admin':
#         delete_manager_user(id)
#         return redirect(url_for('manager.get_all_manager'))
#     else:
#         return render_template('404.html', user=current_user)
#
#
# @register_user.route('/RegisterUser/Insert', methods=['GET', 'POST'])
# @token_required
# def add_register(current_user):
#     if current_user.roles.name == 'admin':
#         form = InsertationForm()
#         if form.validate_on_submit():
#             if request.method == 'POST':
#                 add_manager_user()
#
#                 return redirect(url_for('manager.get_all_manager'))
#         return render_template('add_manager.html', form=form, user=current_user)
#     else:
#         return render_template('404.html', user=current_user)