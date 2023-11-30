# models/ciudad.py
from utils.database import db  # Import the shared instance
from .provincia import Provincia

class Ciudad(db.Model):
    __tablename__ = 'ciudad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_provincia = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)

    provincia = db.relationship('Provincia', backref=db.backref('ciudades', lazy=True))

    def __init__(self, nombre, id_provincia):
        self.nombre = nombre
        self.id_provincia = id_provincia

    # Additional methods and properties can be defined here
