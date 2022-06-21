from flask import render_template, url_for, request, redirect, session
from football_team_manage.manage.form import EditionForm, InsertionLeagueForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.league.services as ml


def get_search_data():
    if check_header():
        data = request.get_json()
    else:
        data = request.form
    return data


def check_search_data(page):
    data = get_search_data()
    if data:
        if session.get('data_league') is None:
            session['data_league'] = data
            session['page'] = 1
            return True
        else:
            if data == session['data_league']:
                session['page'] = page
                return True
            else:
                if page == 1:
                    session.pop('data_league', None)
                    session['data_league'] = data
                    return True
                else:
                    session.pop('data_league', None)
                    session['data_league'] = data
                    session['page'] = '1'
                    return True

    else:
        if session.get('data_league') is None:
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
            list = ml.get_all(page)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            list = ml.get_all(page)
            return render_template('league/league.html', title='Leagues', data=list, user=current_user)
    else:
        if check_header():
            data = session.get('data_league')
            search = data['search']
            page_session = session.get('page')
            list = ml.get_search(int(page_session), search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = session.get('data_league')
            search = data['search']
            page_session = session.get('page')
            list = ml.get_search(int(page_session), search)
            return render_template('league/league.html', title='Leagues', data=list, user=current_user, search=search)


def update(current_user, id):
    if check_header():
        if request.method == 'GET':
            return ml.get(id)
        else:
            return ml.update(id)
    else:
        form = EditionForm()
        if form.validate_on_submit():
            ml.update(id)
            return redirect(url_for('league.update_league', id=id))
        if request.method == 'GET':
            data = ml.get(id)
            form = EditionForm(data=data)
        return render_template('league/update_league.html', title='Update League', form=form, user=current_user, id=id)


def delete(current_user, id):
    if check_header():
        return ml.delete(id)
    else:
        ml.delete(id)
        return redirect(url_for('league.get_all_league'))


def insert(current_user):
    if check_header():
        return ml.add()
    else:
        form = InsertionLeagueForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                ml.add()
                return redirect(url_for('league.get_all_league'))
        return render_template('league/add_league.html', title='Add League', form=form, user=current_user)
