# models/especie.py
from utils.database import db  # Import the shared instance

class Especie(db.Model):
    __tablename__ = 'especie'

    id = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(30), nullable=False)

    def __init__(self, especie):
        self.especie = especie

    # Additional methods and properties can be defined here
