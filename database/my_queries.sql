SELECT user_id, name
FROM Users
WHERE email = 'testuser@example.com'
    AND password_hash = 'hashedpassword123';
    
SELECT u.name,
        COUNT(w.workout_id) AS total_workouts,
        SUM(w.duration_min) AS total_duration_minutes,
        SUM(w.calories_burned) AS total_calories
FROM Users u
JOIN Workouts w ON u.user_id = w.user_id
WHERE u.user_id = 1
GROUP BY u.name;

SELECT quick_workout_id, workout_name, duration_min
FROM QuickWorkouts;

SELECT DATE(start_time) AS workout_date,
        SUM(duration_min) AS total_minutes,
        SUM(calories_burned) AS total_calories
FROM Workouts
WHERE user_id = 1
    AND start_time >= DATE('now', '-7 days')
GROUP BY workout_date
ORDER BY workout_date ASC;


