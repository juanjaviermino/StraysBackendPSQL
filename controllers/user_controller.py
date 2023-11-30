# controllers/user_controller.py
from flask import Blueprint, request, jsonify
from utils.database import db  # Import the shared instance
from models.user import Users
from models.ciudad import Ciudad
from sqlalchemy.exc import IntegrityError

user_blueprint = Blueprint('user_blueprint', __name__)

# POST a new user
@user_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        new_user = Users(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError:
        return jsonify({'message': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# GET all users
@user_blueprint.route('/users', methods=['GET'])
def get_users():
    try:
        users = Users.query.with_entities(Users.id, Users.name, Users.lastname, Users.email, Users.cellphone, Users.role, Ciudad.nombre, Users.ciudad_id).join(Ciudad, Users.ciudad_id == Ciudad.id).all()
        return jsonify([{'id': u.id, 'name': u.name, 'lastname': u.lastname, 'email': u.email, 'cellphone': u.cellphone, 'role': u.role, 'ciudad': u.nombre, 'ciudad_id': u.ciudad_id} for u in users])
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# GET ONE
@user_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = Users.query.join(Ciudad, Users.ciudad_id == Ciudad.id).filter(Users.id == id).first_or_404()
    return jsonify({
        'id': user.id,
        'name': user.name,
        'lastname': user.lastname,
        'email': user.email,
        'password': user.password,  # Be cautious about returning passwords, even hashed ones
        'cellphone': user.cellphone,
        'role': user.role,
        'ciudad_id': user.ciudad.id,
        'ciudad': user.ciudad.nombre,
    }), 200

# DELETE a user by id
@user_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = Users.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# UPDATE a user by id
@user_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    try:
        user = Users.query.get(id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# POST for user authentication
@user_blueprint.route('/users/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.password == password:
        return jsonify({'authenticated': True}), 200
    else:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401


