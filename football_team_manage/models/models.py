from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from football_team_manage import db


class Position(db.Model):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    created_time = Column(DateTime, default=datetime.now())
    player = relationship('Player', backref='position', lazy=False)

    def __str__(self):
        return self.name


class Player(db.Model):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    shirt_number = Column(Integer)
    age = Column(Integer)
    join_time = Column(DateTime, default=datetime.now())
    position_id = Column(Integer, ForeignKey(Position.id), nullable=False)

    def __str__(self):
        return self.name


class LeagueJoin(db.Model):
    __tablename__ = 'league_join'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    join_time = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name


class Roles(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_time = Column(DateTime, default=datetime.now())
    user = relationship('User', backref='roles', lazy=False)

    def __str__(self):
        return self.name


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    user_name = Column(String(50), nullable=False)
    password = Column(String(200), nullable=False)
    created_time = Column(DateTime, default=datetime.now())
    email = Column(String(50))
    phone = Column(String(50))
    status = Column(Boolean, nullable=False)
    role_id = Column(Integer, ForeignKey(Roles.id), nullable=False)


if __name__ == '__main__':
    db.create_all()
