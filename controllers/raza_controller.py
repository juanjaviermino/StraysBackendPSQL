from flask import Blueprint, request, jsonify
from models.raza import Raza
from models.especie import Especie
from utils.database import db

raza_blueprint = Blueprint('raza_blueprint', __name__)

# CREATE 
@raza_blueprint.route('/raza', methods=['POST'])
def create_raza():
    data = request.get_json()
    new_raza = Raza(raza=data['raza'], especie_id=data['especie_id'])
    db.session.add(new_raza)
    db.session.commit()
    return jsonify({
        'message': 'Raza created successfully',
        'raza': {
            'id': new_raza.id,
            'raza': new_raza.raza,
            'especie_id': new_raza.especie_id
        }
    }), 201

# GET ALL
@raza_blueprint.route('/raza', methods=['GET'])
def get_all_razas():
    razas = Raza.query.join(Especie, Raza.especie_id == Especie.id).all()
    raza_list = [{
        'id': raza.id,
        'raza': raza.raza,
        'especie': raza.especie.especie,
        'especie_id': raza.especie_id,
    } for raza in razas]
    return jsonify(raza_list), 200

# GET ONE
@raza_blueprint.route('/raza/<int:id>', methods=['GET'])
def get_raza(id):
    raza = Raza.query.join(Especie, Raza.especie_id == Especie.id).filter(Raza.id == id).first_or_404()
    return jsonify({
        'id': raza.id,
        'raza': raza.raza,
        'especie': raza.especie.especie,
        'especie_id': raza.especie_id,
    }), 200

# EDIT
@raza_blueprint.route('/raza/<int:id>', methods=['PUT'])
def update_raza(id):
    data = request.get_json()
    raza = Raza.query.get_or_404(id)
    raza.raza = data['raza']
    raza.especie_id = data['especie_id']
    db.session.commit()
    return jsonify({
        'message': 'Raza updated successfully',
        'raza': {
            'id': raza.id,
            'raza': raza.raza,
            'especie_id': raza.especie_id
        }
    }), 200

# DELETE
@raza_blueprint.route('/raza/<int:id>', methods=['DELETE'])
def delete_raza(id):
    raza = Raza.query.get_or_404(id)
    db.session.delete(raza)
    db.session.commit()
    return jsonify({'message': 'Raza deleted successfully'}), 200
