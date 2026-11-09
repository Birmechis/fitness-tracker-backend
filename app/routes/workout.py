from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from datetime import datetime
from app.models import Workouts, WorkoutExercises

workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/workouts', methods=['POST'])
@jwt_required()
def create_workout():

    data = request.get_json(silent=True)

    user_id = get_jwt_identity()

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    title = data.get('title')

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title must be a non-empty string"
        }), 400

    try:
        schedule_at = datetime.fromisoformat(data.get('schedule_at'))
    except (ValueError, TypeError):
        return jsonify({
            "error": "Invalid schedule_at format. Use ISO format"
        }), 400

    if title is None or schedule_at is None:
        return jsonify({
            "error": "Missing required fields"
        }), 400

    existing_workout = Workouts.query.filter_by(
        user_id=user_id,
        title=title,
        schedule_at=schedule_at
    ).first()

    if existing_workout:
        return jsonify({
            "error": "Workout already exists"
        }), 409

    new_workout = Workouts(
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
    total_count = Workouts.query.count()
    records = Workouts.query.offset(calculate_offset).limit(limit).all()

    return jsonify({
        "Workouts": [
            {
                "id": workouts.id,
                "user_id": workouts.user_id,
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

@workout_bp.route('/workouts/<int:id>', methods=['GET'])
@jwt_required()
def get_workout_by_id(id):

    workout = Workouts.query.filter_by(id=id).first()

    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404

    return jsonify({
        "id": workout.id,
        "user_id": workout.user_id,
        "title": workout.title,
        "schedule_at": workout.schedule_at,
        "status": workout.status,
        "created_at": workout.created_at.isoformat() if workout.created_at else None,
        "updated_at": workout.updated_at.isoformat() if workout.updated_at else None,
    }), 200

@workout_bp.route('/workouts/<int:id>', methods=['PUT'])
@jwt_required()
def update_workout(id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    title = data.get('title')

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title must be a non-empty string"
        }), 400

    try:
        schedule_at = datetime.fromisoformat(data.get('schedule_at'))
    except (ValueError, TypeError):
        return jsonify({
            "error": "Invalid schedule_at format. Use ISO format"
        }), 400

    user_id = int(get_jwt_identity())

    workout = Workouts.query.filter_by(id=id).first()

    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404

    if workout.user_id != user_id:
        return jsonify({
            "error": "Forbidden"
        }), 403

    workout.title = title
    workout.schedule_at = schedule_at

    db.session.commit()

    return jsonify({
        "id": workout.id,
        "user_id": workout.user_id,
        "title": workout.title,
        "schedule_at": workout.schedule_at,
        "status": workout.status,
        "created_at": workout.created_at.isoformat() if workout.created_at else None,
        "updated_at": workout.updated_at.isoformat() if workout.updated_at else None,
    }), 200

@workout_bp.route('/workouts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_workout(id):

    workout = Workouts.query.filter_by(id=id).first()

    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "msg": "Workout deleted successfully"
    }), 200

@workout_bp.route('/workouts/<int:workout_id>/exercises', methods=['POST'])
@jwt_required()
def add_exercise_to_workout(workout_id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    user_id = get_jwt_identity()

    workout = Workouts.query.filter_by(
        workout_id=workout_id,
        user_id=user_id
    ).first()

    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404

    exercise_id = data.get('exercise_id')
    sets = data.get('sets')
    reps = data.get('reps')
    completed = data.get('completed')

    try:
        exercise = int(exercise_id)
        if exercise <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "exercise_id must be a positive integer"}), 400

    if type(sets) is not int or sets <= 0:
        return jsonify({
            "error": "sets must be a positive integer"
        }), 400

    if type(reps) is not int or reps <= 0:
        return jsonify({
            "error": "reps must be a positive integer"
        }), 400

    if type(completed) is not bool:
        return jsonify({
            "error": "completed must be a boolean"
        }), 400

    existing_workout_exercise = WorkoutExercises.query.filter_by(workout_id=workout_id).first()

    if existing_workout_exercise:
        return jsonify({
            "error": "Workout exercise already exists"
        }), 409

    new_workout_exercise = WorkoutExercises(
        workout_id=workout_id,
        exercise_id=exercise_id,
        sets=sets,
        reps=reps,
        completed=completed
    )

    db.session.add(new_workout_exercise)
    db.session.commit()

    return jsonify({
        "id": new_workout_exercise.id,
        "exercise_id": new_workout_exercise.exercise_id,
        "workout_id": new_workout_exercise.workout_id,
        "sets": new_workout_exercise.sets,
        "reps": new_workout_exercise.reps,
        "completed": new_workout_exercise.completed
    }), 201

@workout_bp.route('/workouts/<int:workout_id>/exercise/<int:we_id>', methods=['PATCH'])
@jwt_required()
def update_workout(workout_id, we_id):

      data = request.get_json(silent=True)

      if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

      sets = data.get('sets')
      reps = data.get('reps')
      completed = data.get('completed')

      user_id = get_jwt_identity()

      workout = Workouts.query.filter_by(
          workout_id=workout_id,
          user_id=user_id
      ).first()

      if not workout:
          return jsonify({
            "error": "Workout not found"
          }), 404

      workout_exercise = WorkoutExercises.query.filter_by(
          workout_id=workout_id,
          id=we_id
      ).first()

      if not workout_exercise:
          return jsonify({
              "error": "Exercise not found"
          }), 404

      if type(sets) is not int or sets <= 0:
          return jsonify({
              "error": "sets must be a positive integer"
          }), 400

      if type(reps) is not int or reps <= 0:
          return jsonify({
              "error": "reps must be a positive integer"
          }), 400

      if type(completed) is not bool:
          return jsonify({
              "error": "completed must be a boolean"
          }), 400

      if workout_exercise.workouts.user_id != user_id:
          return jsonify({
              "error": "Forbidden"
          }), 403

      db.session.commit()

      return jsonify({
          "message": "Workout exercise updated successfully",
          "exercise": {
              "sets": workout_exercise.sets,
              "reps": workout_exercise.reps,
              "completed": workout_exercise.completed
          }
      }), 200

@workout_bp.route('/workouts/<int:workout_id>/exercise/<int:exercise_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id, exercise_id):

    user_id = get_jwt_identity()

    workout_exercise = WorkoutExercises.query.filter_by(exercise_id=exercise_id, workout_id=workout_id).first()

    if not workout_exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    if workout_exercise.workouts.user_id != user_id:
        return jsonify({
            "error": "Forbidden"
        }), 403

    db.session.delete(workout_exercise)
    db.session.commit()

    return '', 204