from football_team_manage.manage.form import UpdateUserForm, InsertionUserForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.admin.services as ma
from flask import render_template, url_for, request, redirect, session


def get_search_data():
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    return data


def check_search_data(page):
    data = get_search_data()
    if data:
        if data['search'] != '':
            if session.get('data_admin') is None:
                session['data_admin'] = data
                session['page'] = 1
                return True
            else:
                if data['search'] == session['data_admin']['search']:
                    session['page'] = page
                    return True
                else:
                    if page == 1:
                        session.pop('data_admin', None)
                        session['data_admin'] = data
                        return True
                    else:
                        session.pop('data_admin', None)
                        session['data_admin'] = data
                        session['page'] = '1'
                        return True
        else:
            session.pop('data_admin', None)
            return False
    else:
        if session.get('data_admin') is None:
            return False
        else:
            if page == 1:
                session['page'] = page
            else:
                session.pop('page', None)
                session['page'] = page
            return True


def get_list(current_user):
    page = request.args.get('page', 1, type=int)
    if not check_search_data(page):
        if check_header():
            list = ma.get_all(page)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            list = ma.get_all(page)
            return render_template('admin/admin.html', title='Administrator', data=list, user=current_user)
    else:
        if check_header():
            data = session.get('data_admin')
            search = data['search']
            page_session = session.get('page')
            list = ma.get_search(int(page_session), search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = session.get('data_admin')
            search = data['search']
            page_session = session.get('page')
            list = ma.get_search(int(page_session), search)
            return render_template('admin/admin.html', title='Administrator', data=list, user=current_user,
                                   search=search)


def update(current_user, id):
    if check_header():
        if request.method == 'POST':
            return ma.update(id, current_user)
        else:
            return ma.get(id)
    else:
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
        return render_template('admin/update_user.html', title='Update Administrator', form=form, user=current_user, id=id)


def insert(current_user):
    if check_header():
        return ma.add()
    else:
        form = InsertionUserForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                ma.add()
                return redirect(url_for('admin.get_all_admin'))
        return render_template('admin/add_user.html', form=form, user=current_user)


def delete(current_user, id):
    if check_header():
        return ma.delete(id, current_user)
    else:
        ma.delete(id, current_user)
        return redirect(url_for('admin.get_all_admin'))
