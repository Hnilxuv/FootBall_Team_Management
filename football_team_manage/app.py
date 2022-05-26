from flask import make_response, jsonify, render_template

from football_team_manage import app
from football_team_manage.manage.home.home import home
from football_team_manage.manage.manager_user.manager_user import manager
from football_team_manage.manage.auth.auth import auth
from football_team_manage.manage.register_user.register_user import register_user
from football_team_manage.manage.test import test


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(manager)
app.register_blueprint(register_user)
app.register_blueprint(test)

app.run(debug=True)
