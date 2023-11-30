# models/user.py
from utils.database import db  # Import the shared instance
from models.products import Products
from models.user import Users

class Sales(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ammount = db.Column(db.Numeric)  # Using the custom numeric type

    product = db.relationship('Products', backref=db.backref('sales', lazy=True))
    user = db.relationship('Users', backref=db.backref('sales', lazy=True))

    def __init__(self, date, product_id, user_id, ammount):
        self.date = date
        self.product_id = product_id
        self.user_id = user_id
        self.ammount = ammount
        

    # Additional methods and properties can be defined here
