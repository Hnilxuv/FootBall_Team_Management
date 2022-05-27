from flask import Blueprint, render_template, url_for, request, redirect, flash
from football_team_manage.manage.manager_user.form import UpdateUserForm, InsertionForm
from football_team_manage.manage.token_required import token_required, has_permission
import football_team_manage.manage.league.controller as ml

league = Blueprint('league', __name__)


@league.route('/League')
@token_required
@has_permission(["admin", "manager", "staff", "register"])
def get_all_manager(current_user):
    dict = ml.get_all()
    if dict:
        list = dict.values()
        return render_template('league.html', data=list, user=current_user)
