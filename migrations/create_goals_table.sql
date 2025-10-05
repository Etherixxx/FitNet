-- Create Goals table
CREATE TABLE IF NOT EXISTS Goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal_type TEXT NOT NULL, -- 'weight_loss', 'muscle_gain', 'strength', 'endurance', 'custom'
    goal_name TEXT NOT NULL,
    target_value REAL,
    current_value REAL DEFAULT 0,
    target_date DATE,
    created_at DATETIME DEFAULT (datetime('now')),
    is_completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
