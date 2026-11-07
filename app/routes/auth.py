from sqlite3 import IntegrityError
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.models import Users
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid or Missing JSON payload"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "error": "Missing username or email or password"
        }), 400

    hashed_password = generate_password_hash(password)

    new_user = Users(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
          "error": "Username and email already exists"
        }), 409

    return jsonify({
        "username": username,
        "email": email,
        "password": password
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid or Missing JSON payload"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Missing email or password"
        }), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "error": "Incorrect password"
        }), 400

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "msg": "logged in successfully",
        "token": token
    }), 200