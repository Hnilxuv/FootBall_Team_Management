from football_team_manage.manage.form import UpdateUserForm, InsertionUserForm, EditionUserForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.register_user.services as mru
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
        if session.get('data_register_user') is None:
            session['data_register_user'] = data
            session['page'] = 1
            return True
        else:
            if data == session['data_register_user']:
                session['page'] = page
                return True
            else:
                if page == 1:
                    session.pop('data_register_user', None)
                    session['data_register_user'] = data
                    return True
                else:
                    session.pop('data_register_user', None)
                    session['data_register_user'] = data
                    session['page'] = '1'
                    return True

    else:
        if session.get('data_register_user') is None:
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
            list = mru.get_all(page)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            list = mru.get_all(page)
            return render_template('register_user/register_user.html', title='Register User', data=list, user=current_user)
    else:
        if check_header():
            data = session.get('data_register_user')
            search = data['search']
            page_session = session.get('page')
            list = mru.get_search(int(page_session), search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = session.get('data_register_user')
            search = data['search']
            page_session = session.get('page')
            list = mru.get_search(int(page_session), search)
            return render_template('register_user/register_user.html', title='Register User', data=list,
                                   user=current_user, search=search)


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