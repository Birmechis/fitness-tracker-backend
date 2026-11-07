from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from datetime import datetime
from app.models import Workout

workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/workouts', methods=['POST'])
@jwt_required()
def create_workout():

    data = request.get_json(silent=True)

    user_id = get_jwt_identity()

    if not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    title = data.get('title')
    schedule_at = datetime.fromisoformat(data.get('schedule_at'))

    if title is None or schedule_at is None:
        return jsonify({
            "error": "Missing required fields"
        }), 400

    existing_workout = Workout.query.filter_by(
        user_id=user_id,
        title=title,
        schedule_at=schedule_at
    ).first()

    if existing_workout:
        return jsonify({
            "error": "Workout already exists"
        }), 409

    new_workout = Workout(
        user_id=user_id,
        title=title,
        schedule_at=schedule_at
    )

    db.session.add(new_workout)
    db.session.commit()

    return jsonify({
        "msg": "Workout created"
    }), 201

@workout_bp.route('/workouts', methods=['GET'])
@jwt_required()
def get_workouts():

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    calculate_offset = (page - 1) * limit
    total_count = Workout.query.count()
    records = Workout.query.offset(calculate_offset).limit(limit).all()

    return jsonify({
        "Workouts": [
            {
                "id": workouts.id,
                "title":  workouts.title,
                "schedule_at": workouts.schedule_at,
                "status": workouts.status,
                "created_at": workouts.created_at.isoformat() if workouts.created_at else None,
                "updated_at": workouts.updated_at.isoformat() if workouts.updated_at else None,
            }for workouts in records
        ],
        "page": page,
        "limit": limit,
        "total": total_count
    }), 200