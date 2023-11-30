from flask import Blueprint, request, jsonify
from models.products import Products
from utils.database import db

product_blueprint = Blueprint('product_blueprint', __name__)

# CREATE 
@product_blueprint.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Products(name=data['name'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'product created successfully', 'product': {'id': new_product.id, 'name': new_product.name}}), 201

# GET ALL
@product_blueprint.route('/product', methods=['GET'])
def get_all_products():
    products = Products.query.all()
    return jsonify([{'id': product.id, 'name': product.name} for product in products]), 200

# GET ONE
@product_blueprint.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Products.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name}), 200

# EDIT
@product_blueprint.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Products.query.get_or_404(id)
    product.name = data['name']
    db.session.commit()
    return jsonify({'message': 'product updated successfully', 'product': {'id': product.id, 'name': product.name}}), 200

# DELETE
@product_blueprint.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Products.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200
