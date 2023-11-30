# models/user.py
from .ciudad import Ciudad
from utils.database import db  # Import the shared instance

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    cellphone = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    ciudad_id = db.Column(db.Integer, db.ForeignKey('ciudad.id'), nullable=False)

    ciudad = db.relationship('Ciudad', backref=db.backref('users', lazy=True))

    def __init__(self, name, lastname, email, password, cellphone, role, ciudad_id):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.cellphone = cellphone
        self.role = role
        self.ciudad_id = ciudad_id

    # Additional methods and properties can be defined here
