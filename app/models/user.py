from datetime import datetime, timezone
from app.extensions import db

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    workouts = db.relationship(
        "Workouts",
        back_populates="users",
    )

    exercises = db.relationship(
        "Exercises",
        back_populates="users",
    )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
