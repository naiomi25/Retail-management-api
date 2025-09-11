from flask import Flask ,jsonify
from flask_cors import CORS
from routes.users import users
from database import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager


load_dotenv()

app = Flask(__name__)

CORS(app,origins="http://localhost:5173")

# configuracion para jwt

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Configuracion de la bd

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicio la bd con la app
db.init_app(app)

with app.app_context():
    db.create_all()

# Registro de Bluprint

app.register_blueprint(users)






if __name__ == "__main__":
    app.run(debug=True)