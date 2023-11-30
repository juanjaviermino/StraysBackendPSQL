#!C:\Users\jmino\AppData\Local\Programs\Python\Python3.9\python.exe
# app.py
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Database configuration

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://straysadmin:3oIOCNl8Rnz8mS6ASzGLWIDEhWakM37d@dpg-cko717oujous73a2h6o0-a.oregon-postgres.render.com/straysdb'
CORS(app)  # Middleware for interacting with your React server


from utils.database import db
db.init_app(app)


# Blueprint registration: 

# Import the provincia_blueprint
from controllers.provincia_controller import provincia_blueprint
app.register_blueprint(provincia_blueprint)

# Import the ciudad blueprint
from controllers.ciudad_controller import ciudad_blueprint
app.register_blueprint(ciudad_blueprint)

# Import the especie blueprint
from controllers.especie_controller import especie_blueprint
app.register_blueprint(especie_blueprint)

# Import the raza blueprint
from controllers.raza_controller import raza_blueprint
app.register_blueprint(raza_blueprint)

# Import the user blueprint
from controllers.user_controller import user_blueprint
app.register_blueprint(user_blueprint)

# Import the products blueprint
from controllers.products_controller import product_blueprint
app.register_blueprint(product_blueprint)

# Import the sales blueprint
from controllers.sales_controller import sales_blueprint
app.register_blueprint(sales_blueprint)

if __name__ == "__main__":
    app.run(debug=True)