# models/raza.py
from .especie import Especie
from utils.database import db  # Import the shared instance

class Raza(db.Model):
    __tablename__ = 'raza'

    id = db.Column(db.Integer, primary_key=True)
    raza = db.Column(db.String(50), nullable=False)
    especie_id = db.Column(db.Integer, db.ForeignKey('especie.id'), nullable=False)

    especie = db.relationship('Especie', backref=db.backref('razas', lazy=True))

    def __init__(self, raza, especie_id):
        self.raza = raza
        self.especie_id = especie_id

    # Additional methods and properties can be defined here
