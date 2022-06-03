from football_team_manage import app
from football_team_manage.manage.admin.routes import admin
from football_team_manage.manage.handler import error
from football_team_manage.manage.home.routes import home
from football_team_manage.manage.league.routes import league
from football_team_manage.manage.manager.routes import manager
from football_team_manage.manage.auth.routes import auth
from football_team_manage.manage.player.routes import player
from football_team_manage.manage.position.routes import position
from football_team_manage.manage.register_user.routes import register_user
from football_team_manage.manage.roles.routes import roles
from football_team_manage.manage.staff.routes import staff

app.register_blueprint(error)
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(manager)
app.register_blueprint(staff)
app.register_blueprint(register_user)
app.register_blueprint(league)
app.register_blueprint(roles)
app.register_blueprint(position)
app.register_blueprint(player)


app.run(debug=True)
