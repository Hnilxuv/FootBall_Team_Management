from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '@#@$Á@ASASAD@#QREDA*12312312312312teared1231231ads_+`<>.?3&EHDJSAJ(&ƯEHU'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:vudinhlinh@localhost/team_manage?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
