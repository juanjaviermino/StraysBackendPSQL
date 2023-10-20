#!C:\Users\jmino\AppData\Local\Programs\Python\Python3.9\python.exe

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
import re
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://straysadmin:3oIOCNl8Rnz8mS6ASzGLWIDEhWakM37d@dpg-cko717oujous73a2h6o0-a.oregon-postgres.render.com/straysdb'
db = SQLAlchemy(app)

CORS(app)  # Middleware for interacting with your React server

# ---------------- MODELS --------------------------

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, name, lastname, email, password):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ammount = db.Column(db.Numeric)  # Using the custom numeric type

    product = db.relationship('Products', backref=db.backref('sales', lazy=True))
    user = db.relationship('Users', backref=db.backref('sales', lazy=True))



# -------------- CONTROLLERS FOR USERS ----------------------

# Route to create a user
@app.route('/users', methods=['POST'])
def createUser():
    data = request.json
    user = Users(**data)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': '¡Te has registrado con éxito!'}), 200
    except IntegrityError as e:
        error_message = str(e.orig)
        if "unique constraint" in error_message.lower():
            return jsonify({'message': 'El e-mail ingresado ya existe, intenta nuevamente'}), 400
        else:
            return jsonify({'message': 'Tuvimos un problema, por favor vuelve a intentar'}), 500

# Route to get all users
@app.route('/users', methods=['GET'])
def getUsers():
    users = Users.query.all()
    user_list = []
    for user in users:
        user_dict = {
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
        }
        user_list.append(user_dict)
    return jsonify(user_list)

# Route to get a single user by id
@app.route('/user/<int:id>', methods=['GET'])
def getUserById(id):
    user = Users.query.get(id)
    if user:
        user_dict = {
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
        }
        return jsonify(user_dict)
    return jsonify({'message': 'User not found'}), 404

# Route to get users based on criteria
@app.route('/userbycriteria', methods=['GET'])
def getUsersByCriteria():
    criteria = request.args.get('criteria', None)
    value = request.args.get('value', None)

    if criteria is None or value is None:
        return jsonify({'message': 'Missing criteria or value in the request.'}), 400

    if criteria == 'name':
        users = Users.query.filter_by(name=value).all()
    elif criteria == 'lastname':
        users = Users.query.filter_by(lastname=value).all()
    elif criteria == 'email':
        users = Users.query.filter_by(email=value).all()
    else:
        return jsonify({'message': 'Invalid criteria provided.'}), 400

    user_list = []
    for user in users:
        user_dict = {
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
        }
        user_list.append(user_dict)

    if user_list:
        return jsonify(user_list)
    else:
        return jsonify({'message': 'No users found based on the provided criteria.'}), 404

# Route to get user password based on email
@app.route('/userbymail', methods=['GET'])
def getPasswordByEmail():
    criteria = request.args.get('criteria', None)
    value = request.args.get('value', None)

    if criteria is None or value is None:
        return jsonify({'message': 'Faltan datos en la solicitud'}), 400

    if criteria == 'email':
        users = Users.query.filter_by(email=value).all()
    else:
        return jsonify({'message': 'Los datos enviados son incorrectos'}), 400

    if users:
        found_password = users[0].password
        pwd_response = {
            'password': found_password,
        }
        return jsonify(pwd_response), 200
    else:
        return jsonify({'message': 'No existen usuarios con el email especificado'}), 404

# Route to delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    try:
        user = Users.query.get(id)
        if user:
            Users.query.filter_by(id=id).delete()
            db.session.commit()
            return jsonify({'message': 'Usuario eliminado satisfactoriamente'}), 200
        else:
            return jsonify({'message': 'El usuario no existe'}), 404
    except Exception as e:
        return jsonify({'message': 'Ocurrió un error eliminando el usuario'}), 500

# Route to update a user
@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    user = Users.query.get(id)
    if user:
        data = request.json
        if 'name' in data:
            user.name = data['name']
        if 'lastname' in data:
            user.lastname = data['lastname']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']
        db.session.commit()
        return jsonify(f'User {user.name} updated successfully'), 200
    return jsonify({'message': 'User not found'}), 404


# -------------- CONTROLLERS FOR PRODUCTS ----------------------

# Route to get all products
@app.route('/products', methods=['GET'])
def getProducts():
    products = Products.query.all()
    product_list = []
    for product in products:
        product_dict = {
            'id': product.id,
            'name': product.name,
        }
        product_list.append(product_dict)
    return jsonify(product_list)

# Route to create a product
@app.route('/products', methods=['POST'])
def createProduct():
    data = request.json
    product = Products(**data)
    
    try:
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Producto creado satisfactoriamente'}), 200
    except IntegrityError as e:
        return jsonify({'message': 'Ocurrió un error creando el producto'}), 500
            

@app.route('/products/<id>', methods=['DELETE'])
def deleteProduct(id):
    try:
        product = Products.query.get(id)
        if product:
            Products.query.filter_by(id=id).delete()
            db.session.commit()
            return jsonify({'message': 'Producto eliminado satisfactoriamente'}), 200
        else:
            return jsonify({'message': 'El producto no existe'}), 404
    except Exception as e:
        return jsonify({'message': 'Ocurrió un error eliminando el producto'}), 500

# -------------- CONTROLLERS FOR SALES ----------------------

@app.route('/sales', methods=['GET'])
def getSales():
    try:
        # Query the Sale, Product, and User tables to retrieve the required information for all sales
        sales = db.session.query(Sales, Products.name, Users.name, Sales.ammount) \
            .join(Products, Sales.product_id == Products.id) \
            .join(Users, Sales.user_id == Users.id) \
            .all()

        sales_info = []
        for sale in sales:
            sale_info = {
                'id': sale[0].id,
                'date': sale[0].date.strftime('%Y-%m-%d'),  # Convert date to string
                'product_name': sale[1],
                'user_name': sale[2],
                'ammount': str(sale[3])  # Convert amount to string
            }
            sales_info.append(sale_info)

        return jsonify(sales_info), 200
    except Exception as e:
        return jsonify({'Hubo un error: ': str(e)}), 500  # Provide the error message for debugging

# Route to create a sale
@app.route('/sales', methods=['POST'])
def createSale():
    data = request.json
    if data['user_id'] == "9999":  # Note that "user_id" is a string in the JSON data
        return jsonify({'message': 'Por favor selecciona un usuario'}), 400
    elif data['product_id'] == "9999":
        return jsonify({'message': 'Por favor selecciona un producto'}), 400
    else:
        sale = Sales(**data)
        try:
            db.session.add(sale)
            db.session.commit()
            return jsonify({'message': 'Venta creada satisfactoriamente'}), 200
        except IntegrityError as e:
            return jsonify({'message': 'Ocurrió un error creando la venta'}), 500


# Route to get the summary of sales between dates
@app.route('/sales_summary', methods=['GET'])
def get_sales_summary():
    begin_date = request.args.get('begin_date', default = None, type = str)
    final_date = request.args.get('final_date', default = None, type = str)

    # Convert the dates from string to datetime objects
    begin_date = datetime.strptime(begin_date, '%Y-%m-%d').date() if begin_date else None
    final_date = datetime.strptime(final_date, '%Y-%m-%d').date() if final_date else None

    if not begin_date or not final_date:
        return jsonify({'error': 'Both begin_date and final_date parameters are required'}), 400

    try:
        # Query the Sale and User tables to retrieve the required information for all sales
        sales_summary = db.session.query(Users.name, func.sum(Sales.ammount)) \
            .join(Sales, Sales.user_id == Users.id) \
            .filter(Sales.date.between(begin_date, final_date)) \
            .group_by(Users.name) \
            .all()

        summary_info = []
        for summary in sales_summary:
            user_summary = {
                'user_name': summary[0],
                'total_ammount': str(summary[1])  # Convert amount to string
            }
            summary_info.append(user_summary)

        return jsonify(summary_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Provide the error message for debugging

if __name__ == "__main__":
    app.run(debug=True)