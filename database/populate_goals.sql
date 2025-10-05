-- Create Goals table if it doesn't exist
CREATE TABLE IF NOT EXISTS Goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal_type TEXT NOT NULL,
    goal_name TEXT NOT NULL,
    target_value REAL,
    current_value REAL DEFAULT 0,
    target_date DATE,
    created_at DATETIME DEFAULT (datetime('now')),
    is_completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Insert 3 goals for each of the 50 users
-- User 1 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(1, 'weight_loss', 'Lose 10kg', 70.0, 75.0, '2024-06-01', 0),
(1, 'strength', 'Bench Press 100kg', 100.0, 85.0, '2024-05-15', 0),
(1, 'endurance', 'Run 5km in 25 minutes', 25.0, 28.0, '2024-04-30', 0);

-- User 2 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(2, 'muscle_gain', 'Gain 5kg muscle', 75.0, 72.0, '2024-07-01', 0),
(2, 'strength', 'Squat 120kg', 120.0, 100.0, '2024-05-30', 0),
(2, 'custom', 'Do 50 push-ups', 50.0, 35.0, '2024-04-15', 0);

-- User 3 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(3, 'weight_loss', 'Reach 65kg', 65.0, 68.0, '2024-08-01', 0),
(3, 'endurance', 'Cycle 50km', 50.0, 30.0, '2024-06-15', 0),
(3, 'strength', 'Deadlift 150kg', 150.0, 130.0, '2024-07-30', 0);

-- User 4 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(4, 'muscle_gain', 'Gain 8kg', 80.0, 74.0, '2024-09-01', 0),
(4, 'custom', 'Plank for 5 minutes', 5.0, 3.0, '2024-05-01', 0),
(4, 'strength', 'Pull-ups 15 reps', 15.0, 8.0, '2024-06-01', 0);

-- User 5 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(5, 'weight_loss', 'Lose 15kg', 65.0, 72.0, '2024-10-01', 0),
(5, 'endurance', 'Marathon under 4 hours', 240.0, 280.0, '2024-11-15', 0),
(5, 'strength', 'Overhead Press 60kg', 60.0, 45.0, '2024-07-01', 0);

-- User 6 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(6, 'custom', 'Yoga 30 days straight', 30.0, 12.0, '2024-05-30', 0),
(6, 'strength', 'Bench Press 80kg', 80.0, 70.0, '2024-06-15', 0),
(6, 'endurance', '10km run under 50 minutes', 50.0, 55.0, '2024-07-01', 0);

-- User 7 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(7, 'muscle_gain', 'Gain 6kg muscle', 78.0, 74.0, '2024-08-15', 0),
(7, 'weight_loss', 'Body fat under 15%', 15.0, 18.0, '2024-09-01', 0),
(7, 'strength', 'Squat 100kg', 100.0, 85.0, '2024-06-30', 0);

-- User 8 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(8, 'endurance', 'Half Marathon under 2 hours', 120.0, 135.0, '2024-08-01', 0),
(8, 'custom', 'Burpees 100 in a row', 100.0, 60.0, '2024-05-15', 0),
(8, 'strength', 'Deadlift 120kg', 120.0, 100.0, '2024-07-15', 0);

-- User 9 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(9, 'weight_loss', 'Lose 12kg', 68.0, 75.0, '2024-09-30', 0),
(9, 'strength', 'Military Press 50kg', 50.0, 40.0, '2024-06-01', 0),
(9, 'custom', 'Handstand for 60 seconds', 60.0, 20.0, '2024-08-01', 0);

-- User 10 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(10, 'muscle_gain', 'Bulk to 85kg', 85.0, 79.0, '2024-12-01', 0),
(10, 'endurance', '5km run under 22 minutes', 22.0, 25.0, '2024-07-01', 0),
(10, 'strength', 'Bench Press 120kg', 120.0, 95.0, '2024-10-01', 0);

-- Continue with similar patterns for users 11-50
-- User 11 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(11, 'weight_loss', 'Cut to 70kg', 70.0, 76.0, '2024-07-15', 0),
(11, 'custom', 'Mountain climbers 200', 200.0, 150.0, '2024-05-01', 0),
(11, 'strength', 'Squat 140kg', 140.0, 110.0, '2024-08-30', 0);

-- User 12 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(12, 'endurance', 'Triathlon completion', 1.0, 0.0, '2024-09-15', 0),
(12, 'strength', 'Pull-ups 20 reps', 20.0, 12.0, '2024-06-15', 0),
(12, 'muscle_gain', 'Gain 4kg lean mass', 73.0, 70.0, '2024-08-01', 0);

-- User 13 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(13, 'custom', 'Daily workouts for 60 days', 60.0, 23.0, '2024-06-30', 0),
(13, 'weight_loss', 'Lose 8kg', 67.0, 72.0, '2024-08-15', 0),
(13, 'strength', 'Deadlift 180kg', 180.0, 140.0, '2024-11-01', 0);

-- User 14 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(14, 'endurance', 'Swim 2km non-stop', 2.0, 1.2, '2024-07-30', 0),
(14, 'strength', 'Overhead Press 70kg', 70.0, 55.0, '2024-09-01', 0),
(14, 'custom', 'Flexibility: Touch toes', 1.0, 0.0, '2024-05-15', 0);

-- User 15 Goals
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(15, 'muscle_gain', 'Gain 10kg', 82.0, 75.0, '2024-12-15', 0),
(15, 'endurance', '15km run completion', 15.0, 10.0, '2024-08-01', 0),
(15, 'strength', 'Bench Press 90kg', 90.0, 75.0, '2024-07-15', 0);

-- Continue with users 16-50 with varied goals
-- I'll add a mix of completed and in-progress goals for variety

-- Users 16-20
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(16, 'weight_loss', 'Lose 6kg', 69.0, 71.0, '2024-06-01', 0),
(16, 'strength', 'Squat bodyweight', 75.0, 70.0, '2024-05-30', 0),
(16, 'custom', 'Meditation 30 days', 30.0, 30.0, '2024-04-30', 1),

(17, 'endurance', 'Marathon completion', 1.0, 1.0, '2024-03-15', 1),
(17, 'muscle_gain', 'Gain 7kg', 80.0, 76.0, '2024-09-01', 0),
(17, 'strength', 'Deadlift 160kg', 160.0, 145.0, '2024-08-15', 0),

(18, 'custom', 'Climb local mountain', 1.0, 0.0, '2024-07-01', 0),
(18, 'weight_loss', 'Body fat under 12%', 12.0, 15.0, '2024-10-01', 0),
(18, 'strength', 'Pull-ups 25 reps', 25.0, 18.0, '2024-08-01', 0),

(19, 'endurance', '10km under 45 minutes', 45.0, 48.0, '2024-06-15', 0),
(19, 'strength', 'Bench Press 110kg', 110.0, 95.0, '2024-09-15', 0),
(19, 'custom', 'Learn proper form', 1.0, 1.0, '2024-04-01', 1),

(20, 'muscle_gain', 'Bulk to 90kg', 90.0, 84.0, '2025-01-01', 0),
(20, 'strength', 'Squat 150kg', 150.0, 120.0, '2024-11-01', 0),
(20, 'endurance', 'Cycle 100km', 100.0, 65.0, '2024-08-30', 0);

-- Users 21-30
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(21, 'weight_loss', 'Cut to 72kg', 72.0, 78.0, '2024-08-01', 0),
(21, 'custom', 'Perfect push-up form', 1.0, 1.0, '2024-03-30', 1),
(21, 'strength', 'Military Press 45kg', 45.0, 35.0, '2024-07-01', 0),

(22, 'endurance', 'Half Ironman', 1.0, 0.0, '2024-10-15', 0),
(22, 'strength', 'Deadlift 200kg', 200.0, 170.0, '2024-12-01', 0),
(22, 'muscle_gain', 'Gain 5kg', 77.0, 74.0, '2024-08-15', 0),

(23, 'custom', 'Flexibility routine daily', 90.0, 45.0, '2024-07-30', 0),
(23, 'weight_loss', 'Lose 14kg', 66.0, 75.0, '2024-11-01', 0),
(23, 'strength', 'Pull-ups 30 reps', 30.0, 15.0, '2024-09-30', 0),

(24, 'endurance', '5km under 20 minutes', 20.0, 23.0, '2024-07-15', 0),
(24, 'strength', 'Bench Press 85kg', 85.0, 85.0, '2024-05-01', 1),
(24, 'custom', 'Calisthenics routine', 1.0, 0.7, '2024-06-30', 0),

(25, 'muscle_gain', 'Gain 12kg', 85.0, 76.0, '2025-02-01', 0),
(25, 'strength', 'Squat 200kg', 200.0, 160.0, '2025-01-15', 0),
(25, 'endurance', 'Ultra marathon', 1.0, 0.0, '2024-12-31', 0);

-- Users 26-35
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(26, 'weight_loss', 'Beach body ready', 73.0, 79.0, '2024-06-01', 0),
(26, 'custom', 'Master handstand', 1.0, 0.3, '2024-09-01', 0),
(26, 'strength', 'Overhead Press 65kg', 65.0, 50.0, '2024-08-15', 0),

(27, 'endurance', 'Tough Mudder race', 1.0, 0.0, '2024-09-30', 0),
(27, 'strength', 'Deadlift 170kg', 170.0, 150.0, '2024-10-15', 0),
(27, 'muscle_gain', 'Visible abs', 1.0, 0.5, '2024-08-01', 0),

(28, 'custom', 'Yoga instructor level', 1.0, 0.4, '2024-12-01', 0),
(28, 'weight_loss', 'Lose 9kg', 68.0, 74.0, '2024-09-15', 0),
(28, 'strength', 'Pull-ups 35 reps', 35.0, 20.0, '2024-11-30', 0),

(29, 'endurance', 'Ironman completion', 1.0, 0.0, '2025-05-01', 0),
(29, 'strength', 'Bench Press 130kg', 130.0, 105.0, '2024-12-15', 0),
(29, 'custom', 'Rock climbing V5', 5.0, 3.0, '2024-10-01', 0),

(30, 'muscle_gain', 'Powerlifter build', 95.0, 87.0, '2025-03-01', 0),
(30, 'strength', 'Squat 180kg', 180.0, 145.0, '2024-11-15', 0),
(30, 'endurance', 'Spartan Race', 1.0, 0.0, '2024-08-15', 0);

-- Users 31-40
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(31, 'weight_loss', 'Cut to 65kg', 65.0, 71.0, '2024-07-30', 0),
(31, 'custom', 'Morning routine 100 days', 100.0, 60.0, '2024-08-30', 0),
(31, 'strength', 'Military Press 55kg', 55.0, 42.0, '2024-09-01', 0),

(32, 'endurance', 'Century bike ride', 100.0, 70.0, '2024-07-15', 0),
(32, 'strength', 'Deadlift 140kg', 140.0, 125.0, '2024-08-30', 0),
(32, 'muscle_gain', 'Lean bulk 6kg', 81.0, 78.0, '2024-11-01', 0),

(33, 'custom', 'Kettlebell certification', 1.0, 0.6, '2024-10-30', 0),
(33, 'weight_loss', 'Marathon weight', 70.0, 76.0, '2024-10-01', 0),
(33, 'strength', 'Pull-ups 40 reps', 40.0, 25.0, '2025-01-01', 0),

(34, 'endurance', 'Olympic triathlon', 1.0, 0.0, '2024-09-01', 0),
(34, 'strength', 'Bench Press 95kg', 95.0, 80.0, '2024-08-01', 0),
(34, 'custom', 'Swim technique mastery', 1.0, 0.7, '2024-07-01', 0),

(35, 'muscle_gain', 'Bodybuilder physique', 88.0, 82.0, '2025-06-01', 0),
(35, 'strength', 'Squat 220kg', 220.0, 180.0, '2025-04-01', 0),
(35, 'endurance', 'CrossFit games qualifier', 1.0, 0.0, '2025-02-01', 0);

-- Users 36-45
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(36, 'weight_loss', 'Wedding ready', 68.0, 73.0, '2024-08-15', 0),
(36, 'custom', 'Dance fitness mastery', 1.0, 0.5, '2024-09-30', 0),
(36, 'strength', 'Overhead Press 48kg', 48.0, 38.0, '2024-07-15', 0),

(37, 'endurance', 'Boston Marathon qualify', 180.0, 200.0, '2025-04-15', 0),
(37, 'strength', 'Deadlift 190kg', 190.0, 165.0, '2024-12-30', 0),
(37, 'muscle_gain', 'Athletic build', 83.0, 79.0, '2024-10-15', 0),

(38, 'custom', 'Gymnastics basics', 1.0, 0.3, '2024-11-15', 0),
(38, 'weight_loss', 'Summer shred', 71.0, 77.0, '2024-06-30', 0),
(38, 'strength', 'Pull-ups 45 reps', 45.0, 28.0, '2024-12-01', 0),

(39, 'endurance', 'Multi-sport athlete', 1.0, 0.0, '2024-11-30', 0),
(39, 'strength', 'Bench Press 105kg', 105.0, 88.0, '2024-09-15', 0),
(39, 'custom', 'Obstacle course racing', 1.0, 0.4, '2024-10-15', 0),

(40, 'muscle_gain', 'Strongman build', 92.0, 86.0, '2025-07-01', 0),
(40, 'strength', 'Squat 250kg', 250.0, 200.0, '2025-06-15', 0),
(40, 'endurance', 'World's Strongest Man', 1.0, 0.0, '2025-12-01', 0);

-- Users 41-50
INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed) VALUES
(41, 'weight_loss', 'Optimal health weight', 69.0, 74.0, '2024-09-01', 0),
(41, 'custom', 'Mindful eating habits', 1.0, 0.8, '2024-06-15', 0),
(41, 'strength', 'Military Press 52kg', 52.0, 43.0, '2024-08-15', 0),

(42, 'endurance', 'Adventure racing', 1.0, 0.0, '2024-10-30', 0),
(42, 'strength', 'Deadlift 155kg', 155.0, 135.0, '2024-09-30', 0),
(42, 'muscle_gain', 'Functional strength', 84.0, 80.0, '2024-12-15', 0),

(43, 'custom', 'Martial arts black belt', 1.0, 0.2, '2026-01-01', 0),
(43, 'weight_loss', 'Competition weight', 72.0, 78.0, '2024-11-15', 0),
(43, 'strength', 'Pull-ups 50 reps', 50.0, 30.0, '2025-03-01', 0),

(44, 'endurance', 'Ultramarathon finish', 1.0, 0.0, '2024-12-15', 0),
(44, 'strength', 'Bench Press 115kg', 115.0, 92.0, '2024-10-30', 0),
(44, 'custom', 'Outdoor adventure skills', 1.0, 0.6, '2024-09-15', 0),

(45, 'muscle_gain', 'Superhero physique', 89.0, 83.0, '2025-08-01', 0),
(45, 'strength', 'Squat 190kg', 190.0, 155.0, '2025-02-15', 0),
(45, 'endurance', 'Decathlon compete', 1.0, 0.0, '2025-07-30', 0),

(46, 'weight_loss', 'Health transformation', 67.0, 72.0, '2024-08-30', 0),
(46, 'custom', 'Lifestyle coaching cert', 1.0, 0.4, '2024-12-31', 0),
(46, 'strength', 'Overhead Press 58kg', 58.0, 46.0, '2024-10-01', 0),

(47, 'endurance', 'Multi-day trek', 1.0, 0.0, '2024-09-15', 0),
(47, 'strength', 'Deadlift 175kg', 175.0, 155.0, '2024-11-30', 0),
(47, 'muscle_gain', 'Explorer physique', 86.0, 81.0, '2025-01-15', 0),

(48, 'custom', 'Fitness influencer', 1.0, 0.5, '2025-06-01', 0),
(48, 'weight_loss', 'Photo shoot ready', 70.0, 75.0, '2024-07-01', 0),
(48, 'strength', 'Pull-ups 55 reps', 55.0, 35.0, '2025-05-01', 0),

(49, 'endurance', 'World championship', 1.0, 0.0, '2025-09-01', 0),
(49, 'strength', 'Bench Press 125kg', 125.0, 98.0, '2024-12-01', 0),
(49, 'custom', 'Perfect training plan', 1.0, 0.7, '2024-11-01', 0),

(50, 'muscle_gain', 'Dream physique', 91.0, 85.0, '2025-09-15', 0),
(50, 'strength', 'Squat 230kg', 230.0, 185.0, '2025-08-30', 0),
(50, 'endurance', 'Fitness hall of fame', 1.0, 0.0, '2026-12-31', 0);
