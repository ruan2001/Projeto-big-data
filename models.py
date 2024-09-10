# models.py
from datetime import datetime  # Importação da biblioteca datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    contact = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    idade_pet = db.Column(db.Integer, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    donation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)


class FosterHome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)


class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # "available", "adopted"
    foster_home_id = db.Column(db.Integer, db.ForeignKey('foster_home.id'), nullable=True)


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # "available", "adopted"
    foster_home_id = db.Column(db.Integer, db.ForeignKey('foster_home.id'), nullable=True)
