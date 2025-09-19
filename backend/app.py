import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from database import db


load_dotenv()

app = Flask(__name__)

CORS(app, origins="http://localhost:5173")

# configuracion para jwt

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Configuracion de la bd

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# inicio la bd con la app
db.init_app(app)
migrate = Migrate(app, db)


from routes.users import users
from routes.entries import entries

# with app.app_context():
#     db.create_all()

# Registro de Bluprint

app.register_blueprint(users)
app.register_blueprint(entries)


@app.route("/")
def check():
    return jsonify({"msg": "api funcionando correctamente"})


if __name__ == "__main__":
    app.run(debug=True)
