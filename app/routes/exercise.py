from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Exercises
from app.extensions import db

exercise_bp = Blueprint('exercise', __name__)

@exercise_bp.route('/exercise', methods=['POST'])
@jwt_required()
def create_exercise():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    user_id = get_jwt_identity()

    exercise_id = data.get('id')

    name = data.get('name')

    if not isinstance(name, str) or not name.strip() or not name:
        return jsonify({
            "error": "Name must be a non-empty string and provided"
        }), 400

    description = data.get('description')

    if not isinstance(description, str) or not name.strip() or not name:
        return jsonify({
            "error": "description must be a non-empty string and provided"
        }), 400

    muscle_group = data.get('muscle_group')

    if not isinstance(muscle_group, str) or not name.strip() or not name:
        return jsonify({
            "error": "muscle group must be a non-empty string and provided"
        }), 400

    existing_exercise = Exercises.query.filter_by(id=exercise_id).first()

    if existing_exercise:
        return jsonify({
            "error": "Exercise already exists"
        }), 409

    new_exercise = Exercises(
        user_id = user_id,
        name = name,
        description = description,
        muscle_group = muscle_group
    )

    db.session.add(new_exercise)
    db.session.commit()

    return jsonify({
        "id": new_exercise.id,
        "name": new_exercise.name,
        "description": new_exercise.description,
        "muscle_group": new_exercise.muscle_group,
        "created_at": new_exercise.created_at.isoformat() if new_exercise.created_at else None,
    }), 201

@exercise_bp.route('/exercise', methods=['GET'])
@jwt_required()
def get_exercise():

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    calculate_offset = (page - 1) * limit
    total_count = Exercises.query.count()
    records = Exercises.query.offset(calculate_offset).limit(limit).all()

    return jsonify({
        "exercises": [
            {
                "id": exercise.id,
                "name": exercise.name,
                "description": exercise.description,
                "muscle_group": exercise.muscle_group,
                "created_at": exercise.created_at.isoformat() if exercise.created_at else None,
                "updated_at": exercise.updated_at.isoformat() if exercise.updated_at else None,
            } for exercise in records
        ],
        "page": page,
        "limit": limit,
        "total": total_count
    }), 200

@exercise_bp.route('/exercise/<int:id>', methods=['GET'])
@jwt_required()
def get_exercise_by_id(id):

    exercise = Exercises.query.filter_by(id=id).first()

    if not exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "description": exercise.description,
        "muscle_group": exercise.muscle_group,
        "created_at": exercise.created_at.isoformat() if exercise.created_at else None,
        "updated_at": exercise.updated_at.isoformat() if exercise.updated_at else None,
    }), 200

@exercise_bp.route('/exercise/<int:id>', methods=['PUT'])
@jwt_required()
def update_exercise(id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    name = data.get('name')

    if not isinstance(name, str) or not name.strip() or not name:
        return jsonify({
            "error": "Name must be a non-empty string and provided"
        }), 400

    description = data.get('description')

    if not isinstance(description, str) or not name.strip() or not name:
        return jsonify({
            "error": "description must be a non-empty string and provided"
        }), 400

    muscle_group = data.get('muscle_group')

    if not isinstance(muscle_group, str) or not name.strip() or not name:
        return jsonify({
            "error": "muscle group must be a non-empty string and provided"
        }), 400

    user_id = int(get_jwt_identity())

    exercise = Exercises.query.filter_by(id=id).first()

    if not exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    if exercise.user_id != user_id:
        return jsonify({
            "error": "Forbidden"
        }), 403

    exercise.name = name
    exercise.description = description
    exercise.muscle_group = muscle_group

    db.session.commit()

    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "description": exercise.description,
        "muscle_group": exercise.muscle_group,
        "created_at": exercise.created_at.isoformat() if exercise.created_at else None,
        "updated_at": exercise.updated_at.isoformat() if exercise.updated_at else None,
    }), 200

@exercise_bp.route('/exercise/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_exercise(id):

    exercise = Exercises.query.filter_by(id=id).first()

    if not exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "msg": "Exercise deleted successfully"
    }), 200