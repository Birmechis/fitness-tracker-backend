from app.extensions import db

class WorkoutExercises(db.Model):

    __tablename__ = "workout_exercise"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    completed = db.Column(db.Boolean, defualt=False)

    workouts = db.relationship(
        "Workouts",
        back_populates="workout_exercises",
    )

    exercises = db.relationship(
        "Exercises",
        back_populates="workout_exercises",
    )

    def __repr__(self):
        return f"WorkoutExercises({self.sets}, {self.reps}, {self.completed})"



