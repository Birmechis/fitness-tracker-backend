from datetime import datetime, timezone
from app.extensions import db

class Workouts(db.Model):

    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    schedule_at = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.String(100), nullable=False, default='pending')
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    users = db.relationship(
        "Users",
        back_populates="workouts",
    )

    workout_exercises = db.relationship(
        "WorkoutExercises",
        back_populates="workouts",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Workout: {self.title}, {self.status}"