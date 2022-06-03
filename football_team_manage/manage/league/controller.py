from flask import render_template, url_for, request, redirect
from football_team_manage.manage.form import EditionForm, InsertionLeagueForm
from football_team_manage.manage.middleware import check_header
import football_team_manage.manage.league.services as ml


def get_list(current_user):
    if check_header():
        list = ml.get_all()
        if list:
            return list
        else:
            return 'not found any record'
    else:
        dict = ml.get_all()
        list = dict.values()
        return render_template('league/league.html', title='Leagues', data=list, user=current_user)


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
