from flask import Flask
from config import Config
from app.extensions import db, jwt

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.workout import workout_bp
    from app.routes.exercise import exercise_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(workout_bp, url_prefix='/api')
    app.register_blueprint(exercise_bp, url_prefix='/api')

    return app

