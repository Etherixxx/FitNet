from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import sqlite3
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Add tojson filter for Jinja2
@app.template_filter('tojson')
def tojson_filter(obj):
    return json.dumps(obj)

# Update template filters for better goal progress calculation
@app.template_filter('goal_progress')
def goal_progress_filter(goal):
    """Calculate progress percentage based on goal direction"""
    if not goal.get('target_value') or goal.get('target_value') == 0:
        return 0
    
    current = goal.get('current_value', 0)
    target = goal.get('target_value')
    direction = goal.get('direction', 'up')
    
    if direction == 'down':
        # For goals that go down (weight loss, faster times)
        if current <= target:
            return 100  # Goal achieved
        else:
            # Assume reasonable starting point for calculation
            start_value = target * 1.5  # 50% higher than target as starting point
            if current >= start_value:
                return 0
            progress = ((start_value - current) / (start_value - target)) * 100
            return max(0, min(100, progress))
    else:
        # For goals that go up (strength, distance, etc.)
        return min(100, (current / target) * 100) if target > 0 else 0

@app.template_filter('goal_display_text')
def goal_display_text_filter(goal):
    """Generate appropriate display text based on goal direction"""
    if not goal.get('target_value'):
        return "No target set"
    
    current = goal.get('current_value', 0)
    target = goal.get('target_value')
    direction = goal.get('direction', 'up')
    
    if direction == 'down':
        remaining = current - target
        if remaining <= 0:
            return "Goal Achieved! 🎉"
        else:
            unit = ""
            if 'kg' in goal.get('goal_name', '').lower():
                unit = "kg"
            elif 'minute' in goal.get('goal_name', '').lower():
                unit = " min"
            elif 'second' in goal.get('goal_name', '').lower():
                unit = " sec"
            return f"{remaining:.1f}{unit} to go"
    else:
        if current >= target:
            return "Goal Achieved! 🎉"
        else:
            progress = (current / target) * 100 if target > 0 else 0
            return f"{progress:.1f}% Complete"

def get_db_connection():
    conn = sqlite3.connect('database/data_source.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form.get('form_type') == 'login':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM Users WHERE email = ? AND password_hash = ?',
            (email, password)
        ).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['user_id']
            session['name'] = f"{user['first_name']} {user['surname']}" if 'first_name' in user and 'surname' in user else 'User'
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    print(f"DEBUG: Dashboard - session user_id: {session.get('user_id')}, session name: {session.get('name')}")  # Debug line
    
    conn = get_db_connection()
    user_data = conn.execute(
        'SELECT first_name, surname, email FROM Users WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()

    print(f"DEBUG: User data from DB: {dict(user_data) if user_data else 'None'}")  # Debug line

    # Get user's full name - prioritize session name, then database
    if session.get('name') and session.get('name') != 'User':
        full_name = session.get('name')
    elif user_data and user_data['first_name'] and user_data['surname']:
        full_name = f"{user_data['first_name']} {user_data['surname']}"
        # Update session with correct name
        session['name'] = full_name
    else:
        full_name = "User"

    print(f"DEBUG: Final full_name: {full_name}")  # Debug line

    # Daily streak: count consecutive days with workouts
    streak_query = '''
        SELECT COUNT(*) as streak FROM (
            SELECT DATE(start_time) as workout_date
            FROM Workouts
            WHERE user_id = ?
            GROUP BY workout_date
            ORDER BY workout_date DESC
        )
        WHERE workout_date >= DATE('now', '-6 days')
    '''
    streak_result = conn.execute(streak_query, (session['user_id'],)).fetchone()
    daily_streak = streak_result['streak'] if streak_result else 0

    # Weekly workouts (last 7 days)
    weekly_workouts_query = (
        'SELECT COUNT(*) FROM Workouts '
        'WHERE user_id = ? AND start_time >= DATE("now", "-6 days")'
    )
    weekly_workouts = conn.execute(weekly_workouts_query, (session['user_id'],)).fetchone()[0]

    # Total time (last 7 days)
    total_time_query = '''
        SELECT SUM(duration_min) FROM Workouts
        WHERE user_id = ? AND start_time >= DATE('now', '-6 days')
    '''
    total_time = conn.execute(total_time_query, (session['user_id'],)).fetchone()[0] or 0

    # Convert total time to hours
    total_time_hours = total_time / 60

    # Recent workouts (latest 3)
    recent_workouts_query = '''
        SELECT workout_type, start_time, duration_min
        FROM Workouts
        WHERE user_id = ?
        ORDER BY start_time DESC
        LIMIT 3
    '''
    recent_workouts = conn.execute(recent_workouts_query, (session['user_id'],)).fetchall()

    conn.close()
    return render_template(
        'dashboard.html',
        user=user_data,
        full_name=full_name,
        daily_streak=daily_streak,
        weekly_workouts=weekly_workouts,
        total_time=total_time,
        total_time_hours=total_time_hours,
        recent_workouts=recent_workouts
    )

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    # Create Goals table if it doesn't exist
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_type TEXT NOT NULL,
                goal_name TEXT NOT NULL,
                target_value REAL,
                current_value REAL DEFAULT 0,
                target_date DATE,
                direction TEXT DEFAULT 'up',
                created_at DATETIME DEFAULT (datetime('now')),
                is_completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        
        # Add direction column if it doesn't exist
        try:
            conn.execute('ALTER TABLE Goals ADD COLUMN direction TEXT DEFAULT "up"')
        except sqlite3.OperationalError:
            # Column already exists
            pass
            
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating Goals table: {e}")

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'personal_info':
            first_name = request.form.get('first_name')
            surname = request.form.get('surname')
            email = request.form.get('email')
            age = request.form.get('age')
            height = request.form.get('height')
            weight = request.form.get('weight')

            # Update the Users table
            conn.execute(
                'UPDATE Users SET first_name = ?, surname = ?, email = ?, age = ? WHERE user_id = ?',
                (first_name, surname, email, age, user_id)
            )

            # Update the Progress table
            conn.execute(
                'UPDATE Progress SET height_cm = ?, weight_kg = ? WHERE user_id = ?',
                (height, weight, user_id)
            )

            conn.commit()
            # Update the session name
            session['name'] = f"{first_name} {surname}"
            
        elif form_type == 'add_goal':
            goal_type = request.form.get('goal_type')
            goal_name = request.form.get('goal_name')
            target_value = request.form.get('target_value')
            target_date = request.form.get('target_date')
            current_value = request.form.get('current_value', 0)
            direction = request.form.get('direction', 'up')

            try:
                # Insert new goal
                conn.execute(
                    'INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, direction) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (user_id, goal_type, goal_name, float(target_value) if target_value else None, 
                     float(current_value) if current_value else 0, target_date if target_date else None, direction)
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error adding goal: {e}")
            
        elif form_type == 'update_goal':
            goal_id = request.form.get('goal_id')
            current_value = request.form.get('current_value')
            is_completed = request.form.get('is_completed') == 'on'

            try:
                # Update goal progress
                conn.execute(
                    'UPDATE Goals SET current_value = ?, is_completed = ? WHERE goal_id = ? AND user_id = ?',
                    (float(current_value) if current_value else 0, is_completed, goal_id, user_id)
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating goal: {e}")
            
        elif form_type == 'delete_goal':
            goal_id = request.form.get('goal_id')
            try:
                conn.execute('DELETE FROM Goals WHERE goal_id = ? AND user_id = ?', (goal_id, user_id))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error deleting goal: {e}")

        conn.close()
        return redirect(url_for('profile'))

    # Get user data
    user_data = conn.execute(
        "SELECT Users.*, Progress.height_cm, Progress.weight_kg FROM Users "
        "LEFT JOIN Progress ON Users.user_id = Progress.user_id "
        "WHERE Users.user_id = ?",
        (user_id,)
    ).fetchone()

    # Get user goals with error handling
    goals = []
    try:
        goals = conn.execute(
            'SELECT * FROM Goals WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching goals: {e}")
        goals = []

    conn.close()
    return render_template('profile.html', user_data=user_data, goals=goals)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
        
    if request.method == 'POST' and request.form.get('form_type') == 'signup':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')

        conn = get_db_connection()

        try:
            # Check if the email is already registered
            existing_user = conn.execute(
                'SELECT * FROM Users WHERE email = ?',
                (email,)
            ).fetchone()

            if existing_user:
                conn.close()
                return render_template('signup.html', error="An account with this email already exists.")

            # Insert the new user - explicitly exclude user_id to let AUTOINCREMENT work
            cursor = conn.execute(
                'INSERT INTO Users (first_name, surname, email, password_hash, age, created_at) VALUES (?, ?, ?, ?, ?, datetime("now"))',
                (first_name, surname, email, password, int(age))
            )

            # Get the user_id of the newly created user
            user_id = cursor.lastrowid
            print(f"DEBUG: Created user with ID: {user_id}")

            if not user_id:
                # If lastrowid doesn't work, try getting the max user_id
                user_id_result = conn.execute('SELECT MAX(user_id) FROM Users WHERE email = ?', (email,)).fetchone()
                user_id = user_id_result[0] if user_id_result and user_id_result[0] else None
                
            if not user_id:
                raise sqlite3.Error("Failed to get user_id after insert")

            # Insert into Progress table - explicitly exclude progress_id
            progress_cursor = conn.execute(
                'INSERT INTO Progress (user_id, date, weight_kg, height_cm) VALUES (?, date("now"), ?, ?)',
                (user_id, float(weight), float(height))
            )
            
            progress_id = progress_cursor.lastrowid
            print(f"DEBUG: Created progress record with ID: {progress_id}")

            conn.commit()

            # Automatically log the user in with proper session data
            session['user_id'] = user_id
            session['name'] = f"{first_name} {surname}"
            print(f"DEBUG: Set session - user_id: {user_id}, name: {first_name} {surname}")

            return redirect(url_for('dashboard'))

        except sqlite3.Error as e:
            conn.rollback()
            print(f"DEBUG: Database error: {str(e)}")
            return render_template('signup.html', error=f"Database error: {str(e)}")

        except ValueError as e:
            conn.rollback()
            print(f"DEBUG: Value error: {str(e)}")
            return render_template('signup.html', error="Please ensure age, height, and weight are valid numbers.")

        finally:
            conn.close()

    return render_template('signup.html')

@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            data = request.json
            workout_type = data.get('workoutType')
            duration = data.get('duration', 0)
            exercises = data.get('sessionLog', [])

            if not workout_type or not exercises:
                return jsonify({'error': 'Missing workout type or exercises'}), 400

            conn = get_db_connection()
            
            # Insert workout record - let database handle workout_id
            workout_cursor = conn.execute(
                'INSERT INTO Workouts (user_id, workout_type, start_time, duration_min) VALUES (?, ?, datetime("now"), ?)',
                (user_id, workout_type, max(1, duration // 60))  # Ensure at least 1 minute
            )
            
            workout_id = workout_cursor.lastrowid
            if not workout_id:
                # Fallback method
                workout_id_result = conn.execute('SELECT MAX(workout_id) FROM Workouts WHERE user_id = ?', (user_id,)).fetchone()
                workout_id = workout_id_result[0] if workout_id_result and workout_id_result[0] else None

            # Insert exercises if Exercises table exists
            if workout_id:
                for exercise in exercises:
                    try:
                        conn.execute(
                            'INSERT INTO Exercises (workout_id, exercise_name, sets, reps, weight_kg, notes) VALUES (?, ?, ?, ?, ?, ?)',
                            (workout_id, exercise['name'], exercise['sets'], exercise['reps'], exercise['weight'], exercise.get('notes', ''))
                        )
                    except sqlite3.OperationalError:
                        # Exercises table might not exist, skip for now
                        print("Exercises table not found, skipping exercise logging")

            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Workout saved successfully'}), 200

        except Exception as e:
            print(f"Error saving workout: {str(e)}")
            return jsonify({'error': 'Failed to save workout'}), 500

    return render_template('log-workout.html')

@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user_id = session['user_id']
    
    # Handle goal updates
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'update_goal_progress':
            goal_id = request.form.get('goal_id')
            current_value = request.form.get('current_value')
            is_completed = request.form.get('is_completed') == 'on'

            try:
                conn.execute(
                    'UPDATE Goals SET current_value = ?, is_completed = ? WHERE goal_id = ? AND user_id = ?',
                    (float(current_value) if current_value else 0, is_completed, goal_id, user_id)
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating goal: {e}")
        
        conn.close()
        return redirect(url_for('progress'))
    
    # Get actual user workout data for charts
    progress_data = conn.execute(
        'SELECT DATE(start_time) AS workout_date, '
        'SUM(duration_min) AS total_minutes, '
        'SUM(calories_burned) AS total_calories, '
        'COUNT(*) as workout_count '
        'FROM Workouts WHERE user_id = ? '
        'GROUP BY workout_date '
        'ORDER BY workout_date ASC',
        (user_id,)
    ).fetchall()

    # Calculate real statistics
    total_workouts = conn.execute(
        'SELECT COUNT(*) FROM Workouts WHERE user_id = ?',
        (user_id,)
    ).fetchone()[0] or 0

    total_time = conn.execute(
        'SELECT SUM(duration_min) FROM Workouts WHERE user_id = ?',
        (user_id,)
    ).fetchone()[0] or 0

    avg_duration = conn.execute(
        'SELECT AVG(duration_min) FROM Workouts WHERE user_id = ?',
        (user_id,)
    ).fetchone()[0] or 0

    # Get user goals
    goals = []
    try:
        goals_result = conn.execute(
            'SELECT * FROM Goals WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
        # Convert Row objects to dictionaries for JSON serialization
        goals = [dict(row) for row in goals_result]
    except sqlite3.Error as e:
        print(f"Error fetching goals: {e}")
        goals = []

    # Calculate goal statistics
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.get('is_completed')])
    active_goals = total_goals - completed_goals

    # Get weekly workout data for chart
    weekly_data_result = conn.execute(
        '''SELECT 
            CASE CAST(strftime('%w', start_time) AS INTEGER)
                WHEN 0 THEN 'Sun'
                WHEN 1 THEN 'Mon'
                WHEN 2 THEN 'Tue'
                WHEN 3 THEN 'Wed'
                WHEN 4 THEN 'Thu'
                WHEN 5 THEN 'Fri'
                WHEN 6 THEN 'Sat'
            END as day_name,
            SUM(duration_min) as total_minutes
        FROM Workouts 
        WHERE user_id = ? AND start_time >= date('now', '-7 days')
        GROUP BY strftime('%w', start_time)
        ORDER BY strftime('%w', start_time)''',
        (user_id,)
    ).fetchall()
    weekly_data = [dict(row) for row in weekly_data_result]

    # Get strength progress data (example with bench press)
    strength_data_result = conn.execute(
        '''SELECT DATE(w.start_time) as workout_date, MAX(e.weight_kg) as max_weight
        FROM Workouts w
        JOIN Exercises e ON w.workout_id = e.workout_id
        WHERE w.user_id = ? AND e.exercise_name LIKE '%bench%press%'
        GROUP BY DATE(w.start_time)
        ORDER BY DATE(w.start_time)''',
        (user_id,)
    ).fetchall()
    strength_data = [dict(row) for row in strength_data_result]

    # Get monthly overview data
    monthly_data_result = conn.execute(
        '''SELECT 
            strftime('%Y-%m', start_time) as month,
            COUNT(*) as workouts,
            SUM(duration_min)/60.0 as hours
        FROM Workouts 
        WHERE user_id = ? AND start_time >= date('now', '-6 months')
        GROUP BY strftime('%Y-%m', start_time)
        ORDER BY month''',
        (user_id,)
    ).fetchall()
    monthly_data = [dict(row) for row in monthly_data_result]

    conn.close()
    
    return render_template('progress.html', 
                         progress_data=progress_data,
                         total_workouts=total_workouts,
                         total_time=total_time,
                         avg_duration=avg_duration,
                         weekly_data=weekly_data,
                         strength_data=strength_data,
                         monthly_data=monthly_data,
                         goals=goals,
                         total_goals=total_goals,
                         completed_goals=completed_goals,
                         active_goals=active_goals)


@app.route('/populate-goals')
def populate_goals():
    """Route to populate the Goals table with sample data"""
    conn = get_db_connection()
    try:
        # First, create the Goals table if it doesn't exist with direction column
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_type TEXT NOT NULL,
                goal_name TEXT NOT NULL,
                target_value REAL,
                current_value REAL DEFAULT 0,
                target_date DATE,
                direction TEXT DEFAULT 'up',
                created_at DATETIME DEFAULT (datetime('now')),
                is_completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        
        # Clear existing goals
        conn.execute('DELETE FROM Goals')
        
        # Insert sample goals with proper directions
        goals_data = []
        
        # Specific goals for first few users with correct directions
        specific_goals = [
            (1, 'weight_loss', 'Lose 10kg', 70.0, 75.0, '2024-06-01', 'down', 0),
            (1, 'strength', 'Bench Press 100kg', 100.0, 85.0, '2024-05-15', 'up', 0),
            (1, 'endurance', 'Run 5km in 25 minutes', 25.0, 28.0, '2024-04-30', 'down', 0),
            
            (2, 'muscle_gain', 'Gain 5kg muscle', 75.0, 72.0, '2024-07-01', 'up', 0),
            (2, 'strength', 'Squat 120kg', 120.0, 100.0, '2024-05-30', 'up', 0),
            (2, 'custom', 'Do 50 push-ups', 50.0, 35.0, '2024-04-15', 'up', 0),
            
            (3, 'weight_loss', 'Reach 65kg', 65.0, 68.0, '2024-08-01', 'down', 0),
            (3, 'endurance', 'Cycle 50km distance', 50.0, 30.0, '2024-06-15', 'up', 0),
            (3, 'strength', 'Deadlift 150kg', 150.0, 130.0, '2024-07-30', 'up', 0),
        ]
        
        goals_data.extend(specific_goals)
        
        # Generate varied goals for users 4-50
        import random
        for user_id in range(4, 51):
            random.seed(user_id)  # Consistent random data
            
            # Weight loss goal (direction: down)
            weight_to_lose = random.randint(5, 15)
            target_weight = random.randint(60, 80)
            current_weight = target_weight + weight_to_lose
            goals_data.append((user_id, 'weight_loss', f'Reach {target_weight}kg', 
                             target_weight, current_weight, '2024-08-01', 'down', 0))
            
            # Strength goal (direction: up)
            exercise = random.choice(['Bench Press', 'Squat', 'Deadlift', 'Overhead Press'])
            target_weight = random.randint(80, 200)
            current_strength = target_weight - random.randint(10, 30)
            goals_data.append((user_id, 'strength', f'{exercise} {target_weight}kg', 
                             target_weight, current_strength, '2024-10-01', 'up', 0))
            
            # Endurance/Time goal (direction: down for time, up for distance)
            if random.choice([True, False]):
                # Time-based goal (faster = better, so direction down)
                distance = random.choice([5, 10, 21])
                target_time = random.randint(20, 180)
                current_time = target_time + random.randint(5, 30)
                goals_data.append((user_id, 'endurance', f'Run {distance}km in {target_time} minutes', 
                                 target_time, current_time, '2024-07-01', 'down', 0))
            else:
                # Distance-based goal (further = better, so direction up)
                target_distance = random.choice([10, 21, 42])
                current_distance = target_distance - random.randint(2, 10)
                goals_data.append((user_id, 'endurance', f'Run {target_distance}km distance', 
                                 target_distance, current_distance, '2024-07-01', 'up', 0))
        
        # Insert all goals
        conn.executemany(
            'INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, direction, is_completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            goals_data
        )
        
        conn.commit()
        
        # Check results
        cursor = conn.execute("SELECT COUNT(*) FROM Goals")
        count = cursor.fetchone()[0]
        
        return f"<h1>Success!</h1><p>Populated {count} goals with proper directions in the database.</p><p><a href='/progress'>View Progress Page</a></p><p><a href='/profile'>View Profile Page</a></p>"
        
    except Exception as e:
        conn.rollback()
        return f"<h1>Error:</h1><p>{str(e)}</p>"
    
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
        return f"<h1>Error:</h1><p>{str(e)}</p>"
    
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
                (height, weight, user_id)
            )

            conn.commit()
            # Update the session name
            session['name'] = f"{first_name} {surname}"
            
        elif form_type == 'add_goal':
            goal_type = request.form.get('goal_type')
            goal_name = request.form.get('goal_name')
            target_value = request.form.get('target_value')
            target_date = request.form.get('target_date')
            current_value = request.form.get('current_value', 0)
            direction = request.form.get('direction', 'up')

            try:
                # Insert new goal
                conn.execute(
                    'INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, direction) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (user_id, goal_type, goal_name, float(target_value) if target_value else None, 
                     float(current_value) if current_value else 0, target_date if target_date else None, direction)
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error adding goal: {e}")
            
        elif form_type == 'update_goal':
            goal_id = request.form.get('goal_id')
            current_value = request.form.get('current_value')
            is_completed = request.form.get('is_completed') == 'on'

            try:
                # Update goal progress
                conn.execute(
                    'UPDATE Goals SET current_value = ?, is_completed = ? WHERE goal_id = ? AND user_id = ?',
                    (float(current_value) if current_value else 0, is_completed, goal_id, user_id)
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating goal: {e}")
            
        elif form_type == 'delete_goal':
            goal_id = request.form.get('goal_id')
            try:
                conn.execute('DELETE FROM Goals WHERE goal_id = ? AND user_id = ?', (goal_id, user_id))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error deleting goal: {e}")

        conn.close()
        return redirect(url_for('profile'))

    # Get user data
    user_data = conn.execute(
        "SELECT Users.*, Progress.height_cm, Progress.weight_kg FROM Users "
        "LEFT JOIN Progress ON Users.user_id = Progress.user_id "
        "WHERE Users.user_id = ?",
        (user_id,)
    ).fetchone()

    # Get user goals with error handling
    goals = []
    try:
        goals = conn.execute(
            'SELECT * FROM Goals WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching goals: {e}")
        goals = []

    conn.close()
    return render_template('profile.html', user_data=user_data, goals=goals)


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
        
    if request.method == 'POST' and request.form.get('form_type') == 'signup':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')

        conn = get_db_connection()

        try:
            # Check if the email is already registered
            existing_user = conn.execute(
                'SELECT * FROM Users WHERE email = ?',
                (email,)
            ).fetchone()

            if existing_user:
                conn.close()
                return render_template('signup.html', error="An account with this email already exists.")

            # Insert the new user - explicitly exclude user_id to let AUTOINCREMENT work
            cursor = conn.execute(
                'INSERT INTO Users (first_name, surname, email, password_hash, age, created_at) VALUES (?, ?, ?, ?, ?, datetime("now"))',
                (first_name, surname, email, password, int(age))
            )

            # Get the user_id of the newly created user
            user_id = cursor.lastrowid
            print(f"DEBUG: Created user with ID: {user_id}")

            if not user_id:
                # If lastrowid doesn't work, try getting the max user_id
                user_id_result = conn.execute('SELECT MAX(user_id) FROM Users WHERE email = ?', (email,)).fetchone()
                user_id = user_id_result[0] if user_id_result and user_id_result[0] else None
                
            if not user_id:
                raise sqlite3.Error("Failed to get user_id after insert")

            # Insert into Progress table - explicitly exclude progress_id
            progress_cursor = conn.execute(
                'INSERT INTO Progress (user_id, date, weight_kg, height_cm) VALUES (?, date("now"), ?, ?)',
                (user_id, float(weight), float(height))
            )
            
            progress_id = progress_cursor.lastrowid
            print(f"DEBUG: Created progress record with ID: {progress_id}")

            conn.commit()

            # Automatically log the user in with proper session data
            session['user_id'] = user_id
            session['name'] = f"{first_name} {surname}"
            print(f"DEBUG: Set session - user_id: {user_id}, name: {first_name} {surname}")

            return redirect(url_for('dashboard'))

        except sqlite3.Error as e:
            conn.rollback()
            print(f"DEBUG: Database error: {str(e)}")
            return render_template('signup.html', error=f"Database error: {str(e)}")

        except ValueError as e:
            conn.rollback()
            print(f"DEBUG: Value error: {str(e)}")
            return render_template('signup.html', error="Please ensure age, height, and weight are valid numbers.")

        finally:
            conn.close()

    return render_template('signup.html')


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            data = request.json
            workout_type = data.get('workoutType')
            duration = data.get('duration', 0)
            exercises = data.get('sessionLog', [])

            if not workout_type or not exercises:
                return jsonify({'error': 'Missing workout type or exercises'}), 400

            conn = get_db_connection()
            
            # Insert workout record - let database handle workout_id
            workout_cursor = conn.execute(
                'INSERT INTO Workouts (user_id, workout_type, start_time, duration_min) VALUES (?, ?, datetime("now"), ?)',
                (user_id, workout_type, max(1, duration // 60))  # Ensure at least 1 minute
            )
            
            workout_id = workout_cursor.lastrowid
            if not workout_id:
                # Fallback method
                workout_id_result = conn.execute('SELECT MAX(workout_id) FROM Workouts WHERE user_id = ?', (user_id,)).fetchone()
                workout_id = workout_id_result[0] if workout_id_result and workout_id_result[0] else None

            # Insert exercises if Exercises table exists
            if workout_id:
                for exercise in exercises:
                    try:
                        conn.execute(
                            'INSERT INTO Exercises (workout_id, exercise_name, sets, reps, weight_kg, notes) VALUES (?, ?, ?, ?, ?, ?)',
                            (workout_id, exercise['name'], exercise['sets'], exercise['reps'], exercise['weight'], exercise.get('notes', ''))
                        )
                    except sqlite3.OperationalError:
                        # Exercises table might not exist, skip for now
                        print("Exercises table not found, skipping exercise logging")

            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Workout saved successfully'}), 200

        except Exception as e:
            print(f"Error saving workout: {str(e)}")
            return jsonify({'error': 'Failed to save workout'}), 500

    return render_template('log-workout.html')


@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user_id = session['user_id']
    
    # Handle goal updates
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'update_goal_progress':
            goal_id = request.form.get('goal_id')
            current_value = request.form.get('current_value')
            is_completed = request.form.get('is_completed') == 'on'

            try:
                conn.execute(
                    'UPDATE Goals SET current_value = ?, is_completed = ? WHERE goal_id = ? AND user_id = ?',
                    (float(current_value) if current_value else 0, is_completed, goal_id, user_id)
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating goal: {e}")
        
        conn.close()
        return redirect(url_for('progress'))
    
    # Get actual user workout data for charts
    progress_data = conn.execute(
        'SELECT DATE(start_time) AS workout_date, '
        'SUM(duration_min) AS total_minutes, '
        'SUM(calories_burned) AS total_calories, '
        'COUNT(*) as workout_count '
        'FROM Workouts WHERE user_id = ? '
        'GROUP BY workout_date '
        'ORDER BY workout_date ASC',
        (user_id,)
    ).fetchall()

    # Calculate real statistics
    total_workouts = conn.execute(
        'SELECT COUNT(*) FROM Workouts WHERE user_id = ?',
        (user_id,)
    ).fetchone()[0] or 0

    total_time = conn.execute(
        'SELECT SUM(duration_min) FROM Workouts WHERE user_id = ?',
        (user_id,)
    ).fetchone()[0] or 0

    avg_duration = conn.execute(
        'SELECT AVG(duration_min) FROM Workouts WHERE user_id = ?',
        (user_id,)
    ).fetchone()[0] or 0

    # Get user goals
    goals = []
    try:
        goals_result = conn.execute(
            'SELECT * FROM Goals WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
        # Convert Row objects to dictionaries for JSON serialization
        goals = [dict(row) for row in goals_result]
    except sqlite3.Error as e:
        print(f"Error fetching goals: {e}")
        goals = []

    # Calculate goal statistics
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.get('is_completed')])
    active_goals = total_goals - completed_goals

    # Get weekly workout data for chart
    weekly_data_result = conn.execute(
        '''SELECT 
            CASE CAST(strftime('%w', start_time) AS INTEGER)
                WHEN 0 THEN 'Sun'
                WHEN 1 THEN 'Mon'
                WHEN 2 THEN 'Tue'
                WHEN 3 THEN 'Wed'
                WHEN 4 THEN 'Thu'
                WHEN 5 THEN 'Fri'
                WHEN 6 THEN 'Sat'
            END as day_name,
            SUM(duration_min) as total_minutes
        FROM Workouts 
        WHERE user_id = ? AND start_time >= date('now', '-7 days')
        GROUP BY strftime('%w', start_time)
        ORDER BY strftime('%w', start_time)''',
        (user_id,)
    ).fetchall()
    weekly_data = [dict(row) for row in weekly_data_result]

    # Get strength progress data (example with bench press)
    strength_data_result = conn.execute(
        '''SELECT DATE(w.start_time) as workout_date, MAX(e.weight_kg) as max_weight
        FROM Workouts w
        JOIN Exercises e ON w.workout_id = e.workout_id
        WHERE w.user_id = ? AND e.exercise_name LIKE '%bench%press%'
        GROUP BY DATE(w.start_time)
        ORDER BY DATE(w.start_time)''',
        (user_id,)
    ).fetchall()
    strength_data = [dict(row) for row in strength_data_result]

    # Get monthly overview data
    monthly_data_result = conn.execute(
        '''SELECT 
            strftime('%Y-%m', start_time) as month,
            COUNT(*) as workouts,
            SUM(duration_min)/60.0 as hours
        FROM Workouts 
        WHERE user_id = ? AND start_time >= date('now', '-6 months')
        GROUP BY strftime('%Y-%m', start_time)
        ORDER BY month''',
        (user_id,)
    ).fetchall()
    monthly_data = [dict(row) for row in monthly_data_result]

    conn.close()
    
    return render_template('progress.html', 
                         progress_data=progress_data,
                         total_workouts=total_workouts,
                         total_time=total_time,
                         avg_duration=avg_duration,
                         weekly_data=weekly_data,
                         strength_data=strength_data,
                         monthly_data=monthly_data,
                         goals=goals,
                         total_goals=total_goals,
                         completed_goals=completed_goals,
                         active_goals=active_goals)


@app.route('/populate-goals')
def populate_goals():
    """Route to populate the Goals table with sample data"""
    conn = get_db_connection()
    try:
        # First, create the Goals table if it doesn't exist with direction column
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_type TEXT NOT NULL,
                goal_name TEXT NOT NULL,
                target_value REAL,
                current_value REAL DEFAULT 0,
                target_date DATE,
                direction TEXT DEFAULT 'up',
                created_at DATETIME DEFAULT (datetime('now')),
                is_completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        
        # Clear existing goals
        conn.execute('DELETE FROM Goals')
        
        # Insert sample goals with proper directions
        goals_data = []
        
        # Specific goals for first few users with correct directions
        specific_goals = [
            (1, 'weight_loss', 'Lose 10kg', 70.0, 75.0, '2024-06-01', 'down', 0),
            (1, 'strength', 'Bench Press 100kg', 100.0, 85.0, '2024-05-15', 'up', 0),
            (1, 'endurance', 'Run 5km in 25 minutes', 25.0, 28.0, '2024-04-30', 'down', 0),
            
            (2, 'muscle_gain', 'Gain 5kg muscle', 75.0, 72.0, '2024-07-01', 'up', 0),
            (2, 'strength', 'Squat 120kg', 120.0, 100.0, '2024-05-30', 'up', 0),
            (2, 'custom', 'Do 50 push-ups', 50.0, 35.0, '2024-04-15', 'up', 0),
            
            (3, 'weight_loss', 'Reach 65kg', 65.0, 68.0, '2024-08-01', 'down', 0),
            (3, 'endurance', 'Cycle 50km distance', 50.0, 30.0, '2024-06-15', 'up', 0),
            (3, 'strength', 'Deadlift 150kg', 150.0, 130.0, '2024-07-30', 'up', 0),
        ]
        
        goals_data.extend(specific_goals)
        
        # Generate varied goals for users 4-50
        import random
        for user_id in range(4, 51):
            random.seed(user_id)  # Consistent random data
            
            # Weight loss goal (direction: down)
            weight_to_lose = random.randint(5, 15)
            target_weight = random.randint(60, 80)
            current_weight = target_weight + weight_to_lose
            goals_data.append((user_id, 'weight_loss', f'Reach {target_weight}kg', 
                             target_weight, current_weight, '2024-08-01', 'down', 0))
            
            # Strength goal (direction: up)
            exercise = random.choice(['Bench Press', 'Squat', 'Deadlift', 'Overhead Press'])
            target_weight = random.randint(80, 200)
            current_strength = target_weight - random.randint(10, 30)
            goals_data.append((user_id, 'strength', f'{exercise} {target_weight}kg', 
                             target_weight, current_strength, '2024-10-01', 'up', 0))
            
            # Endurance/Time goal (direction: down for time, up for distance)
            if random.choice([True, False]):
                # Time-based goal (faster = better, so direction down)
                distance = random.choice([5, 10, 21])
                target_time = random.randint(20, 180)
                current_time = target_time + random.randint(5, 30)
                goals_data.append((user_id, 'endurance', f'Run {distance}km in {target_time} minutes', 
                                 target_time, current_time, '2024-07-01', 'down', 0))
            else:
                # Distance-based goal (further = better, so direction up)
                target_distance = random.choice([10, 21, 42])
                current_distance = target_distance - random.randint(2, 10)
                goals_data.append((user_id, 'endurance', f'Run {target_distance}km distance', 
                                 target_distance, current_distance, '2024-07-01', 'up', 0))
        
        # Insert all goals
        conn.executemany(
            'INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, direction, is_completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            goals_data
        )
        
        conn.commit()
        
        # Check results
        cursor = conn.execute("SELECT COUNT(*) FROM Goals")
        count = cursor.fetchone()[0]
        
        return f"<h1>Success!</h1><p>Populated {count} goals with proper directions in the database.</p><p><a href='/progress'>View Progress Page</a></p><p><a href='/profile'>View Profile Page</a></p>"
        
    except Exception as e:
        conn.rollback()
        return f"<h1>Error:</h1><p>{str(e)}</p>"
    
    finally:
        conn.close()

# Update template filters for better goal progress calculation
@app.template_filter('goal_progress')
def goal_progress_filter(goal):
    """Calculate progress percentage based on goal direction"""
    if not goal.get('target_value') or goal.get('target_value') == 0:
        return 0
    
    current = goal.get('current_value', 0)
    target = goal.get('target_value')
    direction = goal.get('direction', 'up')
    
    if direction == 'down':
        # For goals that go down (weight loss, faster times)
        if current <= target:
            return 100  # Goal achieved
        else:
            # Assume reasonable starting point for calculation
            start_value = target * 1.5  # 50% higher than target as starting point
            if current >= start_value:
                return 0
            progress = ((start_value - current) / (start_value - target)) * 100
            return max(0, min(100, progress))
    else:
        # For goals that go up (strength, distance, etc.)
        return min(100, (current / target) * 100) if target > 0 else 0

@app.template_filter('goal_display_text')
def goal_display_text_filter(goal):
    """Generate appropriate display text based on goal direction"""
    if not goal.get('target_value'):
        return "No target set"
    
    current = goal.get('current_value', 0)
    target = goal.get('target_value')
    direction = goal.get('direction', 'up')
    
    if direction == 'down':
        remaining = current - target
        if remaining <= 0:
            return "Goal Achieved! 🎉"
        else:
            unit = ""
            if 'kg' in goal.get('goal_name', '').lower():
                unit = "kg"
            elif 'minute' in goal.get('goal_name', '').lower():
                unit = " min"
            elif 'second' in goal.get('goal_name', '').lower():
                unit = " sec"
            return f"{remaining:.1f}{unit} to go"
    else:
        if current >= target:
            return "Goal Achieved! 🎉"
        else:
            progress = (current / target) * 100 if target > 0 else 0
            return f"{progress:.1f}% Complete"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
