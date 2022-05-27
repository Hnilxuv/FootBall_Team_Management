from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.config['SECRET_KEY'] = '@#@$Á@ASASAD@#QREDA*123123123123123&EHDJSAJ(&ƯEHU'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:vudinhlinh@localhost/team_manage?charset=utf8mb4"
app.config["SQlALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
