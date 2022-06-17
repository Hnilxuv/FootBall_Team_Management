from flask import render_template, url_for, request, redirect
from football_team_manage.manage.form import EditionPlayerForm, InsertionPlayerForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.player.services as mp


def get_list(current_user):
    page = request.args.get('page', 1, type=int)
    if request.method == 'GET':
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
            data = request.get_json()
            search = data['search']
            list = mp.get_search(page, search)
            if list:
                return list
            else:
                return 'not found any record'
        else:
            data = request.form
            search = data['search']
            list = mp.get_search(page, search)
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
