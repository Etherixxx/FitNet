-- Fix Users table to ensure proper AUTOINCREMENT
CREATE TABLE IF NOT EXISTS Users_new (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    age INTEGER,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- Copy existing data if any
INSERT INTO Users_new (first_name, surname, email, password_hash, age, created_at)
SELECT first_name, surname, email, password_hash, age, created_at FROM Users;

-- Drop old table and rename new one
DROP TABLE Users;
ALTER TABLE Users_new RENAME TO Users;

-- Fix Progress table
CREATE TABLE IF NOT EXISTS Progress_new (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    weight_kg REAL,
    height_cm REAL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Copy existing data if any
INSERT INTO Progress_new (user_id, date, weight_kg, height_cm)
SELECT user_id, date, weight_kg, height_cm FROM Progress;

-- Drop old table and rename new one
DROP TABLE Progress;
ALTER TABLE Progress_new RENAME TO Progress;

-- Fix Workouts table
CREATE TABLE IF NOT EXISTS Workouts_new (
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    workout_type TEXT NOT NULL,
    start_time DATETIME DEFAULT (datetime('now')),
    duration_min INTEGER DEFAULT 0,
    calories_burned INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Copy existing data if any
INSERT INTO Workouts_new (user_id, workout_type, start_time, duration_min, calories_burned)
SELECT user_id, workout_type, start_time, duration_min, calories_burned FROM Workouts;

-- Drop old table and rename new one
DROP TABLE Workouts;
ALTER TABLE Workouts_new RENAME TO Workouts;

-- Create Exercises table if it doesn't exist
CREATE TABLE IF NOT EXISTS Exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    exercise_name TEXT NOT NULL,
    sets INTEGER DEFAULT 1,
    reps INTEGER DEFAULT 1,
    weight_kg REAL DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (workout_id) REFERENCES Workouts(workout_id)
);
