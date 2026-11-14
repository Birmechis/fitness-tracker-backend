# Fitness Tracker API

A Flask-based REST API for tracking workouts, exercises, and fitness progress.

## Features

- User authentication (signup/login) with JWT
- Create and manage workouts
- Add exercises to workouts with sets, reps, and completion tracking
- Comment on workouts
- Progress reports with completion statistics
- Workout history tracking

## Tech Stack

- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.7.4
- SQLite database
- Python-dotenv 1.2.4

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory:
```
DATABASE_URL=sqlite:///instance/db.sqlite3
JWT_SECRET_KEY=your-secret-key-here
```

3. Run the application:
```bash
python run.py
```

The server will start at `http://127.0.0.1:5000` in debug mode.

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Workouts
- `POST /api/workouts` - Create workout
- `GET /api/workouts` - List workouts (paginated)
- `GET /api/workouts/<id>` - Get workout by ID
- `PUT /api/workouts/<id>` - Update workout
- `DELETE /api/workouts/<id>` - Delete workout

### Workout Exercises
- `POST /api/workouts/<workout_id>/exercises` - Add exercise to workout
- `GET /api/workouts_exercise` - List all workout exercises
- `PATCH /api/workouts/<workout_id>/exercises/<we_id>` - Update workout exercise
- `DELETE /api/workouts/<workout_id>/exercises/<exercise_id>` - Remove exercise from workout

### Workout Comments
- `POST /api/workouts/<workout_id>/comments` - Add comment to workout
- `GET /api/comments` - List all comments
- `DELETE /api/workouts/<workout_id>/comments/<comments_id>` - Delete comment

### Exercises
- `POST /api/exercise` - Create exercise
- `GET /api/exercise` - List exercises (paginated)
- `GET /api/exercise/<id>` - Get exercise by ID
- `PUT /api/exercise/<id>` - Update exercise
- `DELETE /api/exercise/<id>` - Delete exercise

### Reports
- `GET /api/reports/progress` - Get progress report (with optional date filters)
- `GET /api/reports/history` - Get workout history

## Database Models

- **Users** - User accounts with authentication
- **Workouts** - Scheduled workouts with status tracking
- **Exercises** - Exercise definitions with muscle groups
- **WorkoutExercises** - Junction table linking workouts and exercises
- **WorkoutComments** - User comments on workouts

## Authentication

All endpoints except `/api/auth/signup` and `/api/auth/login` require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```
