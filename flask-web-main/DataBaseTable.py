from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from settings import db,app

class UserInfo(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

with app.app_context():
    db.create_all()