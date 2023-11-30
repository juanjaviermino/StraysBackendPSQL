# controllers/sales_controller.py
from flask import Blueprint, request, jsonify
from utils.database import db  # Import the shared instance
from models.sales import Sales
from models.user import Users
from models.products import Products
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import func

sales_blueprint = Blueprint('sales_blueprint', __name__)

@sales_blueprint.route('/sales', methods=['GET'])
def getSales():
    try:
        # Query the Sale, Product, and User tables to retrieve the required information for all sales
        sales = db.session.query(Sales, Products.name, Users.name, Users.lastname, Sales.ammount) \
            .join(Products, Sales.product_id == Products.id) \
            .join(Users, Sales.user_id == Users.id) \
            .all()

        sales_info = []
        for sale in sales:
            sale_info = {
                'id': sale[0].id,
                'date': sale[0].date.strftime('%Y-%m-%d'),  # Convert date to string
                'product_name': sale[1],
                'user_name': sale[2] + ' ' + sale[3],
                'ammount': str(sale[4])  # Convert amount to string
            }
            sales_info.append(sale_info)

        return jsonify(sales_info), 200
    except Exception as e:
        return jsonify({'Hubo un error: ': str(e)}), 500  # Provide the error message for debugging

# Route to create a sale
@sales_blueprint.route('/sales', methods=['POST'])
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
@sales_blueprint.route('/sales_summary', methods=['GET'])
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
        sales_summary = db.session.query(Users.name, Users.lastname, func.sum(Sales.ammount)) \
            .join(Sales, Sales.user_id == Users.id) \
            .filter(Sales.date.between(begin_date, final_date)) \
            .group_by(Users.name, Users.lastname) \
            .all()

        summary_info = []
        for summary in sales_summary:
            user_summary = {
                'user_name': summary[0] + ' ' + summary[1] ,
                'total_ammount': str(summary[2])  # Convert amount to string
            }
            summary_info.append(user_summary)

        return jsonify(summary_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Provide the error message for debugging