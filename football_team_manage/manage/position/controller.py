from flask import render_template, url_for, request, redirect, session
from football_team_manage.manage.form import EditionForm, InsertionPositionForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.position.services as mp


def get_search_data():
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    return data


def check_search_data(page):
    data = get_search_data()
    if data:
        if session.get('data_position') is None:
            session['data_position'] = data
            session['page'] = 1
            return True
        else:
            if data == session['data_position']:
                session['page'] = page
                return True
            else:
                if page == 1:
                    session.pop('data_position', None)
                    session['data_position'] = data
                    return True
                else:
                    session.pop('data_position', None)
                    session['data_position'] = data
                    session['page'] = '1'
                    return True

    else:
        if session.get('data_position') is None:
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
            list = mp.get_all(page)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            list = mp.get_all(page)
            return render_template('position/position.html', title='Position', data=list, user=current_user)
    else:
        if check_header():
            data = session.get('data_position')
            search = data['search']
            page_session = session.get('page')
            list = mp.get_search(int(page_session), search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = session.get('data_position')
            search = data['search']
            page_session = session.get('page')
            list = mp.get_search(int(page_session), search)
            return render_template('position/position.html', title='Position', data=list, user=current_user, search=search)


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
