# models/provincia.py
from utils.database import db  # Import the shared instance

class Provincia(db.Model):
    __tablename__ = 'provincia'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(35), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    # Additional methods and properties can be defined here
