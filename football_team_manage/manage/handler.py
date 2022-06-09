from flask import render_template, Blueprint

from football_team_manage.manage.middleware import token_required, check_header

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
@token_required
def page_not_found(current_user, _error):
    if check_header():
        return '404 not found', 404
    else:
        return render_template('error/404.html', user=current_user), 404


@error.app_errorhandler(500)
@token_required
def page_not_found(current_user, _error):
    if check_header():
        return '404 not found', 500
    else:
        return render_template('error/500.html', user=current_user), 500


@error.app_errorhandler(400)
@token_required
def page_not_found(current_user, _error):
    if check_header():
        return '404 not found', 400
    else:
        return render_template('error/404.html', user=current_user), 400


@error.app_errorhandler(403)
@token_required
def page_not_found(current_user, _error):
    if check_header():
        return '404 not found', 403
    else:
        return render_template('error/404.html', user=current_user), 403