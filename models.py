from config import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    register_date = db.Column(db.DateTime)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(100))
    body = db.Column(db.Text)
    created_date = db.Column(db.DateTime)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(100))
    comment = db.Column(db.Text)
    article = db.relationship('Articles')
    article_id = db.Column(db.Integer, db.ForeignKey(Articles.id))
    created_date = db.Column(db.DateTime)
