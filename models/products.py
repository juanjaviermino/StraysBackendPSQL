# models/user.py
from utils.database import db  # Import the shared instance

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    # Additional methods and properties can be defined here
