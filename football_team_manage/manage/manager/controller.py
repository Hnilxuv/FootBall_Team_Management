from football_team_manage.manage.form import UpdateUserForm, InsertionUserForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.manager.services as mm
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
        if session.get('data_manager') is None:
            session['data_manager'] = data
            session['page'] = 1
            return True
        else:
            if data == session['data_manager']:
                session['page'] = page
                return True
            else:
                if page == 1:
                    session.pop('data_manager', None)
                    session['data_manager'] = data
                    return True
                else:
                    session.pop('data_manager', None)
                    session['data_manager'] = data
                    session['page'] = '1'
                    return True

    else:
        if session.get('data_manager') is None:
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
            list = mm.get_all(page)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            list = mm.get_all(page)
            return render_template('manager/manager.html', title='Manager', data=list, user=current_user)
    else:
        if check_header():
            data = session.get('data_manager')
            search = data['search']
            page_session = session.get('page')
            list = mm.get_search(int(page_session), search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = session.get('data_manager')
            search = data['search']
            page_session = session.get('page')
            list = mm.get_search(int(page_session), search)
            return render_template('manager/manager.html', title='Manager', data=list, user=current_user,
                                   search=search)


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
                return redirect(url_for('manager.get_all_manager'))
        return render_template('manager/add_user.html', form=form, user=current_user)


def delete(id):
    if check_header():
        return mm.delete(id)
    else:
        mm.delete(id)
        return redirect(url_for('manager.get_all_manager'))