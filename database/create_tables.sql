-- Drop existing tables if they exist
DROP TABLE IF EXISTS Exercises;
DROP TABLE IF EXISTS Workouts;
DROP TABLE IF EXISTS Progress;
DROP TABLE IF EXISTS Users;

-- Create Users table with proper AUTOINCREMENT
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    age INTEGER,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- Create Progress table with proper AUTOINCREMENT
CREATE TABLE Progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    weight_kg REAL,
    height_cm REAL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Workouts table with proper AUTOINCREMENT
CREATE TABLE Workouts (
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    workout_type TEXT NOT NULL,
    start_time DATETIME DEFAULT (datetime('now')),
    duration_min INTEGER DEFAULT 0,
    calories_burned INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Exercises table with proper AUTOINCREMENT
CREATE TABLE Exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    exercise_name TEXT NOT NULL,
    sets INTEGER DEFAULT 1,
    reps INTEGER DEFAULT 1,
    weight_kg REAL DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (workout_id) REFERENCES Workouts(workout_id)
);
