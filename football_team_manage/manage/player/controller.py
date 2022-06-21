from flask import render_template, url_for, request, redirect, session
from football_team_manage.manage.form import EditionPlayerForm, InsertionPlayerForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.player.services as mp


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
            if session.get('data_player') is None:
                session['data_player'] = data
                session['page'] = 1
                return True
            else:
                if data == session['data_player']:
                    session['page'] = page
                    return True
                else:
                    if page == 1:
                        session.pop('data_player', None)
                        session['data_player'] = data
                        return True
                    else:
                        session.pop('data_player', None)
                        session['data_player'] = data
                        session['page'] = '1'
                        return True
        else:
            session.pop('data_player', None)
            return False
    else:
        if session.get('data_player') is None:
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
            return render_template('player/player.html', title='Player', data=list, user=current_user)
    else:
        if check_header():
            data = session.get('data_player')
            search = data['search']
            page_session = session.get('page')
            list = mp.get_search(int(page_session), search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = session.get('data_player')
            search = data['search']
            page_session = session.get('page')
            list = mp.get_search(int(page_session), search)
            return render_template('player/player.html', title='Player', data=list, user=current_user, search=search)


def update(current_user, id):
    if check_header():
        if request.method == 'GET':
            return mp.get(id)
        else:
            return mp.update(id)
    else:
        form = EditionPlayerForm()
        if form.validate_on_submit():
            mp.update(id)
            return redirect(url_for('player.update_player', id=id))
        if request.method == 'GET':
            data = mp.get(id)
            form = EditionPlayerForm(data=data)
        return render_template('player/add_player.html', title='Update Player', form=form, user=current_user, id=id)


def delete(current_user, id):
    if check_header():
        return mp.delete(id)
    else:
        mp.delete(id)
        return redirect(url_for('player.get_all_player'))


def insert(current_user):
    if check_header():
        return mp.add()
    else:
        form = InsertionPlayerForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                mp.add()
                return redirect(url_for('player.get_all_player'))
        return render_template('player/add_player.html', title='Add Player', form=form, user=current_user)
