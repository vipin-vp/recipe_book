# app/models.py
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='recipes')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
