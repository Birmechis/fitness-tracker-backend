from datetime import datetime, timezone
from app.extensions import db

class WorkoutComments(db.Model):

    __tablename__ = 'workout_comments'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    workouts = db.relationship(
        'Workouts',
        back_populates='workout_comments',
    )

    users = db.relationship(
        'Users',
        backref='workout_comments',
    )

    def __repr__(self):
        return f"Workout comment: {self.comment}"