from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://straysadmin:3oIOCNl8Rnz8mS6ASzGLWIDEhWakM37d@dpg-cko717oujous73a2h6o0-a.oregon-postgres.render.com/straysdb'
db = SQLAlchemy(app)

CORS(app)  # Middleware for interacting with your React server

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, name, lastname, email, password):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password

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
        error_message = str(e)
        if re.search(r"Violation of UNIQUE KEY constraint", error_message, re.I):
            return jsonify({'message': 'El e-mail ingresado ya existe, intenta nuevamente'}), 400  # HTTP 400 Bad Request
        else:
            # Handle other IntegrityErrors or database errors as needed
            return jsonify({'message': 'Tuvimos un problema, porfavor vuelve a intentar'}), 500  # HTTP 500 Internal Server Error

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
    user = Users.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(f'User {user.name} has been deleted'), 200
    return jsonify({'message': 'User not found'}), 404

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

if __name__ == "__main__":
    app.run(debug=True)