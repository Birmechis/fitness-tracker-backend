from datetime import datetime, timezone
from app.extensions import db

class Exercises(db.Model):

    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    muscle_group = db.Column(db.String(100), nullable=False)
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
        back_populates="exercises",
    )

    workout_exercises = db.relationship(
        "WorkoutExercises",
        back_populates="exercises",
    )

    def __repr__(self):
        return f"Exercise: {self.name}, {self.description}"