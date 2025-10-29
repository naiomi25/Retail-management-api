from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from models.model_users import User

users = Blueprint("users", __name__, url_prefix="/api/users")


@users.route("/register", methods=["POST","OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return jsonify({}), 200 
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se envió JSON"}), 400
        required_fields = ["name", "email", "password", "user_name"]

        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"error": "Faltan datos por rellenar"}),400

        user = db.session.scalar(select(User).where((User.email == data["email"])))
        if user:
            return jsonify({"error": "Usuario ya existe"}), 409

        hashed_password = generate_password_hash(data["password"])

        new_user = User(
            name=data["name"],
            email=data["email"],
            password=hashed_password,
            user_name=data["user_name"],
        )
        db.session.add(new_user)
        print("Nuevo usuario:", new_user.serialize())
        db.session.commit()
        return jsonify({"message": "usuario creado correctamente"}), 201

    except Exception as e:
        print("Error en el servidor", e)
        return jsonify({"error": "error al cargar el registro"}), 500


@users.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
     

        if not email or not password:
            return jsonify({"msg": " falta email o contraseña"}), 400

        user = db.session.scalar(select(User).where(User.email == email))
        print("datos recibidos del back", user)

        if not user:
            return jsonify({"msg": "no se encuentra usuario en la base de datos"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "contraseña incorrecta"}), 401

        access_token = create_access_token(identity=str(user.id))
        print(access_token)

        return jsonify(
            {"msn": "usuario logeado correctamente", "access_token": access_token,'user': user.serialize() }
        )

    except Exception as e:
        print("error al obtener los datos", e)
        return jsonify({"msn": "error al obtener los datos"}), 500
