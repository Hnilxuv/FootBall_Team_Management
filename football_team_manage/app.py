from flask import make_response, jsonify, render_template

from football_team_manage import app
from football_team_manage.manage.admin_user.routes import admin
from football_team_manage.manage.home.routes import home
from football_team_manage.manage.manager_user.routes import manager
from football_team_manage.manage.auth.routes import auth
from football_team_manage.manage.register_user.routes import register_user
from football_team_manage.manage.staff.routes import staff
from football_team_manage.manage.test import test
from football_team_manage.manage.token_required import token_required


@app.errorhandler(404)
@token_required
def page_not_found(current_user, e):
    return render_template('404.html', user=current_user), 404


@app.errorhandler(500)
@token_required
def page_not_found(e, current_user):
    return render_template('404.html', user=current_user), 500


app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(manager)
app.register_blueprint(register_user)
app.register_blueprint(test)
app.register_blueprint(admin)
app.register_blueprint(staff)


app.run(debug=True)
