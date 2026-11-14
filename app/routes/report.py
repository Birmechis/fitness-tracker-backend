from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Workouts

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports/progress', methods=['GET'])
@jwt_required()
def get_report_progress():

    user_id = int(get_jwt_identity())

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Workouts.query.filter_by(user_id=user_id)

    if start_date:
        start_dt = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
        query = query.filter(Workouts.schedule_at >= start_dt)

    if end_date:
        end_dt = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
        query = query.filter(Workouts.schedule_at <= end_dt)

    workouts = query.all()

    total = len(workouts)
    completed = sum(1 for w in workouts if w.status == 'completed')
    percentage = round((completed / total) * 100, 2) if total > 0 else 0

    return jsonify({
        "workouts": [
            {
                "id": w.id,
                "title": w.title,
                "schedule_at": w.schedule_at,
                "status": w.status,
                "created_at": w.created_at,
            } for w in workouts
        ],
        "total_workouts": total,
        "completed_workouts": completed,
        "completion_percentage": percentage,
    }), 200

@report_bp.route('/reports/history', methods=['GET'])
@jwt_required()
def get_report_history():

    user_id = int(get_jwt_identity())
    history = datetime.now(timezone.utc)

    workouts = (
        Workouts.query
        .filter(
            Workouts.user_id==user_id,
            Workouts.schedule_at < history
        )
        .order_by(Workouts.schedule_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": w.id,
            "title": w.title,
            "schedule_at": w.schedule_at,
            "status": w.status,
            "created_at": w.created_at,
        } for w in workouts
    ]), 200