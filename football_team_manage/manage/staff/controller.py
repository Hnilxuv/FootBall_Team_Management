from football_team_manage.manage.form import UpdateUserForm, InsertionUserForm, EditionUserForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.staff.services as ms
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
        if session.get('data_staff') is None:
            session['data_staff'] = data
            session['page'] = 1
            return True
        else:
            if data == session['data_staff']:
                session['page'] = page
                return True
            else:
                if page == 1:
                    session.pop('data_staff', None)
                    session['data_staff'] = data
                    return True
                else:
                    session.pop('data_staff', None)
                    session['data_staff'] = data
                    session['page'] = '1'
                    return True

    else:
        if session.get('data_staff') is None:
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
            list = ms.get_all(page)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            list = ms.get_all(page)
            return render_template('staff/staff.html', title='Staff', data=list, user=current_user)
    else:
        if check_header():
            data = session.get('data_staff')
            search = data['search']
            page_session = session.get('page')
            list = ms.get_search(int(page_session), search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = session.get('data_staff')
            search = data['search']
            page_session = session.get('page')
            list = ms.get_search(int(page_session), search)
            return render_template('staff/staff.html', title='Staff', data=list, user=current_user, search=search)


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
