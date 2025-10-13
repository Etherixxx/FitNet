from flask import Flask, render_template, redirect, url_for, request, session, jsonify, send_from_directory
import sqlite3
import json
import traceback


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Add tojson filter for Jinja2
@app.template_filter('tojson')
def tojson_filter(obj):
    return json.dumps(obj)


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

    # Recent workouts (latest 20) - Fixed datetime and numeric handling
    recent_workouts_query = '''
        SELECT workout_id, workout_type, start_time, duration_min
        FROM Workouts
        WHERE user_id = ?
        ORDER BY start_time DESC
        LIMIT 20
    '''
    recent_workouts_raw = conn.execute(recent_workouts_query, (session['user_id'],)).fetchall()
    
    # Convert to list of dictionaries and parse datetime strings + ensure numeric types
    recent_workouts = []
    for workout in recent_workouts_raw:
        workout_dict = dict(workout)
        
        # Parse the datetime string from SQLite
        if workout_dict['start_time']:
            try:
                from datetime import datetime
                # SQLite datetime format: "2024-01-15 14:30:00"
                workout_dict['start_time'] = datetime.strptime(workout_dict['start_time'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                # If parsing fails, set to None so template shows 'Recently'
                workout_dict['start_time'] = None
        
        # Ensure duration_min is an integer for template calculations
        try:
            workout_dict['duration_min'] = int(workout_dict['duration_min']) if workout_dict['duration_min'] else 0
        except (ValueError, TypeError):
            workout_dict['duration_min'] = 0
        
        # Ensure workout_id is an integer
        try:
            workout_dict['workout_id'] = int(workout_dict['workout_id']) if workout_dict['workout_id'] else 0
        except (ValueError, TypeError):
            workout_dict['workout_id'] = 0
        
        recent_workouts.append(workout_dict)

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
                created_at DATETIME DEFAULT (datetime('now')),
                is_completed BOOLEAN DEFAULT 0,
                goal_direction TEXT DEFAULT 'up',
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        # Add goal_direction column if it doesn't exist
        try:
            conn.execute('ALTER TABLE Goals ADD COLUMN goal_direction TEXT DEFAULT "up"')
        except sqlite3.OperationalError:
            pass  # Column already exists
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
            goal_direction = request.form.get('goal_direction', 'up')

            try:
                # Insert new goal
                conn.execute(
                    'INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, goal_direction) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (user_id, goal_type, goal_name, float(target_value) if target_value else None, 
                     float(current_value) if current_value else 0, target_date if target_date else None, goal_direction)
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
    """Route to populate the Goals table with sample data based on real user profiles"""
    conn = get_db_connection()
    try:
        # First, ensure the Goals table has the goal_direction column
        conn.execute('''
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
                goal_direction TEXT DEFAULT 'up',
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        
        # Add goal_direction column if it doesn't exist
        try:
            conn.execute('ALTER TABLE Goals ADD COLUMN goal_direction TEXT DEFAULT "up"')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Clear ALL existing goals to start fresh
        conn.execute('DELETE FROM Goals')
        
        # Get all users with their profile data
        users_data = conn.execute('''
            SELECT u.user_id, u.first_name, u.surname, u.age, 
                   p.weight_kg, p.height_cm
            FROM Users u
            LEFT JOIN Progress p ON u.user_id = p.user_id
            WHERE u.user_id <= 50
            ORDER BY u.user_id
        ''').fetchall()
        
        goals_data = []
        import random
        
        for user in users_data:
            user_id = user['user_id']
            # Convert to float and handle None/empty values properly
            current_weight = float(user['weight_kg']) if user['weight_kg'] else random.randint(60, 100)
            height = float(user['height_cm']) if user['height_cm'] else random.randint(150, 190)
            age = int(user['age']) if user['age'] else random.randint(18, 65)
            
            # Calculate BMI to determine realistic goals - now both are numbers
            bmi = current_weight / ((height/100) ** 2) if height and height > 0 else 25
            
            random.seed(user_id)  # Consistent random data per user
            goal_types = ['weight_loss', 'muscle_gain', 'strength', 'endurance', 'custom']
            selected_types = random.sample(goal_types, 3)
            
            for goal_type in selected_types:
                if goal_type == 'weight_loss':
                    # Base target weight on current weight and BMI
                    if bmi > 25:  # Overweight, significant weight loss goal
                        target_weight = current_weight - random.randint(8, 20)
                    elif bmi > 23:  # Slightly overweight, moderate goal
                        target_weight = current_weight - random.randint(3, 10)
                    else:  # Normal weight, small cut
                        target_weight = current_weight - random.randint(2, 6)
                    
                    target_weight = max(50, target_weight)  # Don't go below 50kg
                    goals_data.append((user_id, goal_type, f'Reach {target_weight:.1f}kg', 
                                     round(target_weight, 1), round(current_weight, 1), '2024-08-01', 0, 'down'))
                                     
                elif goal_type == 'muscle_gain':
                    # Base muscle gain on current weight
                    if current_weight < 65:  # Underweight, significant gain
                        target_weight = current_weight + random.randint(8, 15)
                    elif current_weight < 80:  # Normal, moderate gain
                        target_weight = current_weight + random.randint(5, 12)
                    else:  # Already heavy, small lean gain
                        target_weight = current_weight + random.randint(3, 8)
                    
                    goals_data.append((user_id, goal_type, f'Bulk to {target_weight:.1f}kg', 
                                     round(target_weight, 1), round(current_weight, 1), '2024-09-01', 0, 'up'))
                                     
                elif goal_type == 'strength':
                    exercise = random.choice(['Bench Press', 'Squat', 'Deadlift', 'Overhead Press'])
                    
                    # Base strength goals on bodyweight and gender assumptions
                    if exercise == 'Bench Press':
                        # Assume current is 0.8-1.2x bodyweight, target is 1.0-1.5x
                        current_strength = current_weight * random.uniform(0.8, 1.2)
                        target_strength = current_weight * random.uniform(1.0, 1.5)
                    elif exercise == 'Squat':
                        # Squats are typically stronger
                        current_strength = current_weight * random.uniform(1.0, 1.5)
                        target_strength = current_weight * random.uniform(1.3, 2.0)
                    elif exercise == 'Deadlift':
                        # Deadlifts are typically strongest
                        current_strength = current_weight * random.uniform(1.2, 1.8)
                        target_strength = current_weight * random.uniform(1.5, 2.2)
                    else:  # Overhead Press
                        # OHP is typically weakest
                        current_strength = current_weight * random.uniform(0.5, 0.8)
                        target_strength = current_weight * random.uniform(0.7, 1.0)
                    
                    # Ensure target > current and round to 1 decimal place
                    current_strength = round(current_strength, 1)
                    target_strength = round(target_strength, 1)
                    if target_strength <= current_strength:
                        target_strength = current_strength + random.randint(5, 15)
                        target_strength = round(target_strength, 1)
                    
                    goals_data.append((user_id, goal_type, f'{exercise} {target_strength}kg', 
                                     target_strength, current_strength, '2024-10-01', 0, 'up'))
                                     
                elif goal_type == 'endurance':
                    if random.choice([True, False]):  # Time-based goals (down direction)
                        distance = random.choice([5, 10, 21])
                        
                        # Base running times on fitness level (estimated from BMI and age)
                        fitness_factor = (30 - bmi) + (40 - age) / 10  # Higher is better
                        
                        if distance == 5:
                            base_time = max(20, 35 - fitness_factor)
                            current_time = base_time + random.randint(3, 10)
                            target_time = base_time + random.randint(0, 5)
                        elif distance == 10:
                            base_time = max(40, 70 - fitness_factor * 2)
                            current_time = base_time + random.randint(5, 15)
                            target_time = base_time + random.randint(0, 8)
                        else:  # Half marathon
                            base_time = max(90, 140 - fitness_factor * 3)
                            current_time = base_time + random.randint(10, 30)
                            target_time = base_time + random.randint(0, 15)
                        
                        goals_data.append((user_id, goal_type, f'Run {distance}km in {target_time:.1f} minutes', 
                                         round(target_time, 1), round(current_time, 1), '2024-07-01', 0, 'down'))
                    else:  # Distance-based goals (up direction)
                        current_distance = random.randint(10, 40)
                        target_distance = current_distance + random.randint(10, 30)
                        
                        goals_data.append((user_id, goal_type, f'Cycle {target_distance}km', 
                                         round(target_distance, 1), round(current_distance, 1), '2024-07-01', 0, 'up'))
                                         
                else:  # custom goals
                    custom_options = [
                        ('100 push-ups', 100, lambda: random.randint(30, 80), 'up'),
                        ('Plank 5 minutes', 5, lambda: random.randint(1, 4), 'up'),
                        ('Body fat 12%', 12, lambda: random.randint(15, 25), 'down'),
                        ('Yoga 30 days', 30, lambda: random.randint(5, 25), 'up'),
                        ('Body fat 15%', 15, lambda: random.randint(18, 28), 'down'),
                        ('Pull-ups 20 reps', 20, lambda: random.randint(5, 18), 'up'),
                        ('Daily steps 10000', 10000, lambda: random.randint(4000, 8000), 'up'),
                        ('Water 3L daily', 3, lambda: random.uniform(1.5, 2.8), 'up'),
                    ]
                    
                    goal_name, target, current_func, direction = random.choice(custom_options)
                    current_val = current_func()
                    
                    # Ensure proper relationship between current and target and round values
                    if direction == 'up' and current_val >= target:
                        current_val = target - random.randint(1, 5)
                    elif direction == 'down' and current_val <= target:
                        current_val = target + random.randint(1, 5)
                    
                    goals_data.append((user_id, goal_type, goal_name, 
                                     round(target, 1), round(current_val, 1), '2024-06-01', 0, direction))

        # Insert all goals with explicit direction values
        conn.executemany(
            'INSERT INTO Goals (user_id, goal_type, goal_name, target_value, current_value, target_date, is_completed, goal_direction) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            goals_data
        )
        
        conn.commit()
        
        # Verify with a few sample users
        verification_users = [1, 2, 3]
        verification_text = ""
        
        for uid in verification_users:
            user_info = conn.execute(
                'SELECT u.first_name, p.weight_kg FROM Users u LEFT JOIN Progress p ON u.user_id = p.user_id WHERE u.user_id = ?', 
                (uid,)
            ).fetchone()
            
            user_goals = conn.execute(
                'SELECT goal_name, target_value, current_value, goal_direction FROM Goals WHERE user_id = ? ORDER BY goal_type', 
                (uid,)
            ).fetchall()
            
            verification_text += f"<h4>User {uid} ({user_info['first_name'] if user_info else 'Unknown'}) - Weight: {user_info['weight_kg'] if user_info else 'N/A'}kg</h4>"
            for goal in user_goals:
                verification_text += f"• {goal['goal_name']}: {goal['current_value']:.1f} → {goal['target_value']:.1f} ({goal['goal_direction']})<br>"
            verification_text += "<br>"
        
        # Check total count
        cursor = conn.execute("SELECT COUNT(*) FROM Goals")
        count = cursor.fetchone()[0]
        
        return f"<h1>Success!</h1><p>Populated {count} realistic goals based on user profiles.</p>{verification_text}<p><a href='/progress'>View Progress Page</a></p><p><a href='/profile'>View Profile Page</a></p>"
        
    except Exception as e:
        conn.rollback()
        return f"<h1>Error:</h1><p>{str(e)}</p><p>Traceback: {traceback.format_exc()}</p>"
    
    finally:
        conn.close()

@app.route('/populate-workouts')
def populate_workouts():
    """Route to populate the Workouts and Exercises tables with realistic data"""
    conn = get_db_connection()
    try:
        # Clear existing workout and exercise data
        conn.execute('DELETE FROM Exercises')
        conn.execute('DELETE FROM Workouts')
        
        # Ensure the Workouts table has proper AUTOINCREMENT for workout_id
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Workouts_New (
                workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                workout_type TEXT NOT NULL,
                start_time DATETIME,
                end_time DATETIME,
                duration_min INTEGER,
                calories_burned INTEGER,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        
        # Check if we need to migrate from old table structure
        try:
            conn.execute('INSERT INTO Workouts_New SELECT * FROM Workouts WHERE 1=0')  # Test if structures match
            conn.execute('DROP TABLE IF EXISTS Workouts_Old')
            conn.execute('ALTER TABLE Workouts RENAME TO Workouts_Old')
            conn.execute('ALTER TABLE Workouts_New RENAME TO Workouts')
        except:
            # If migration fails, just use the new table
            conn.execute('DROP TABLE IF EXISTS Workouts')
            conn.execute('ALTER TABLE Workouts_New RENAME TO Workouts')
        
        conn.commit()
        
        # Get all users
        users = conn.execute('SELECT user_id FROM Users WHERE user_id <= 50').fetchall()
        
        import random
        from datetime import datetime, timedelta
        
        # Define workout types and their appropriate exercises
        workout_types = {
            'strength': {
                'exercises': [
                    {'name': 'Bench Press', 'type': 'reps', 'sets_range': (3, 5), 'reps_range': (6, 12), 'weight_range': (40, 120)},
                    {'name': 'Squat', 'type': 'reps', 'sets_range': (3, 5), 'reps_range': (8, 15), 'weight_range': (50, 150)},
                    {'name': 'Deadlift', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (5, 8), 'weight_range': (60, 180)},
                    {'name': 'Overhead Press', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (6, 10), 'weight_range': (25, 80)},
                    {'name': 'Barbell Row', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (8, 12), 'weight_range': (40, 100)},
                    {'name': 'Pull-ups', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (3, 12), 'weight_range': (0, 20)},
                    {'name': 'Dips', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (6, 15), 'weight_range': (0, 25)},
                    {'name': 'Bicep Curls', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (10, 15), 'weight_range': (10, 40)},
                    {'name': 'Tricep Extensions', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (10, 15), 'weight_range': (8, 35)},
                    {'name': 'Leg Press', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (12, 20), 'weight_range': (80, 200)}
                ],
                'duration_range': (45, 90),
                'calories_range': (200, 400)
            },
            'cardio': {
                'exercises': [
                    {'name': 'Treadmill Running', 'type': 'time', 'sets_range': (1, 1), 'time_range': (15, 45), 'weight_range': (0, 0)},
                    {'name': 'Cycling', 'type': 'time', 'sets_range': (1, 1), 'time_range': (20, 60), 'weight_range': (0, 0)},
                    {'name': 'Elliptical', 'type': 'time', 'sets_range': (1, 1), 'time_range': (15, 40), 'weight_range': (0, 0)},
                    {'name': 'Rowing Machine', 'type': 'time', 'sets_range': (1, 1), 'time_range': (10, 30), 'weight_range': (0, 0)},
                    {'name': 'Stair Climber', 'type': 'time', 'sets_range': (1, 1), 'time_range': (10, 25), 'weight_range': (0, 0)},
                    {'name': 'Jump Rope', 'type': 'time', 'sets_range': (3, 5), 'time_range': (2, 5), 'weight_range': (0, 0)},
                    {'name': 'Burpees', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (8, 20), 'weight_range': (0, 0)},
                    {'name': 'Mountain Climbers', 'type': 'time', 'sets_range': (3, 4), 'time_range': (0.5, 2), 'weight_range': (0, 0)},
                    {'name': 'High Knees', 'type': 'time', 'sets_range': (3, 4), 'time_range': (0.5, 2), 'weight_range': (0, 0)}
                ],
                'duration_range': (30, 75),
                'calories_range': (250, 500)
            },
            'flexibility': {
                'exercises': [
                    {'name': 'Forward Fold', 'type': 'time', 'sets_range': (1, 3), 'time_range': (0.5, 2), 'weight_range': (0, 0)},
                    {'name': 'Downward Dog', 'type': 'time', 'sets_range': (1, 3), 'time_range': (1, 3), 'weight_range': (0, 0)},
                    {'name': 'Pigeon Pose', 'type': 'time', 'sets_range': (2, 2), 'time_range': (1, 3), 'weight_range': (0, 0)},
                    {'name': 'Cat-Cow Stretch', 'type': 'reps', 'sets_range': (1, 2), 'reps_range': (8, 15), 'weight_range': (0, 0)},
                    {'name': 'Seated Spinal Twist', 'type': 'time', 'sets_range': (2, 2), 'time_range': (0.5, 2), 'weight_range': (0, 0)},
                    {'name': 'Hamstring Stretch', 'type': 'time', 'sets_range': (2, 2), 'time_range': (1, 2), 'weight_range': (0, 0)},
                    {'name': 'Shoulder Rolls', 'type': 'reps', 'sets_range': (1, 2), 'reps_range': (10, 20), 'weight_range': (0, 0)},
                    {'name': 'Hip Circles', 'type': 'reps', 'sets_range': (1, 2), 'reps_range': (8, 15), 'weight_range': (0, 0)}
                ],
                'duration_range': (20, 60),
                'calories_range': (50, 150)
            },
            'hiit': {
                'exercises': [
                    {'name': 'Burpees', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 1), 'weight_range': (0, 0)},
                    {'name': 'Jump Squats', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 1), 'weight_range': (0, 0)},
                    {'name': 'Push-ups', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 1), 'weight_range': (0, 0)},
                    {'name': 'Mountain Climbers', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 1), 'weight_range': (0, 0)},
                    {'name': 'High Knees', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 1), 'weight_range': (0, 0)},
                    {'name': 'Plank Jacks', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 1), 'weight_range': (0, 0)},
                    {'name': 'Jumping Jacks', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 1), 'weight_range': (0, 0)}
                ],
                'duration_range': (20, 45),
                'calories_range': (200, 400)
            },
            'functional': {
                'exercises': [
                    {'name': 'Kettlebell Swings', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (15, 25), 'weight_range': (8, 24)},
                    {'name': 'Turkish Get-ups', 'type': 'reps', 'sets_range': (2, 3), 'reps_range': (3, 8), 'weight_range': (8, 20)},
                    {'name': 'Farmer\'s Walk', 'type': 'time', 'sets_range': (3, 4), 'time_range': (0.5, 2), 'weight_range': (15, 40)},
                    {'name': 'Bear Crawl', 'type': 'time', 'sets_range': (3, 4), 'time_range': (0.5, 1.5), 'weight_range': (0, 0)},
                    {'name': 'Box Jumps', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (8, 15), 'weight_range': (0, 0)},
                    {'name': 'Battle Ropes', 'type': 'time', 'sets_range': (3, 4), 'time_range': (0.5, 2), 'weight_range': (0, 0)},
                    {'name': 'Medicine Ball Slams', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (10, 20), 'weight_range': (6, 15)}
                ],
                'duration_range': (30, 60),
                'calories_range': (180, 350)
            },
            'core': {
                'exercises': [
                    {'name': 'Plank', 'type': 'time', 'sets_range': (3, 4), 'time_range': (0.5, 3), 'weight_range': (0, 0)},
                    {'name': 'Side Plank', 'type': 'time', 'sets_range': (4, 6), 'time_range': (0.5, 2), 'weight_range': (0, 0)},
                    {'name': 'Russian Twists', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (20, 40), 'weight_range': (0, 10)},
                    {'name': 'Dead Bug', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (10, 20), 'weight_range': (0, 0)},
                    {'name': 'Bicycle Crunches', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (20, 40), 'weight_range': (0, 0)},
                    {'name': 'Leg Raises', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (10, 20), 'weight_range': (0, 0)},
                    {'name': 'Bird Dog', 'type': 'reps', 'sets_range': (3, 4), 'reps_range': (8, 15), 'weight_range': (0, 0)}
                ],
                'duration_range': (20, 45),
                'calories_range': (100, 250)
            }
        }
        
        # Define the date range for September and October 2025
        sep_start = datetime(2025, 9, 1)
        oct_end = datetime(2025, 10, 31)
        total_days = (oct_end - sep_start).days + 1
        
        # Generate workouts for each user
        for user in users:
            user_id = user['user_id']
            random.seed(user_id)  # Consistent data per user
            
            # Generate 8-20 workouts per user scattered across September-October 2025
            num_workouts = random.randint(8, 20)
            
            # Generate random dates within September-October 2025
            workout_dates = []
            for i in range(num_workouts):
                # Random day within the 61-day period (Sep 1 - Oct 31)
                days_offset = random.randint(0, total_days - 1)
                workout_date = sep_start + timedelta(days=days_offset)
                
                # Add random hour between 6 AM and 10 PM
                start_hour = random.randint(6, 22)
                start_minute = random.randint(0, 59)
                workout_datetime = workout_date.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
                workout_dates.append(workout_datetime)
            
            # Sort workout dates chronologically
            workout_dates.sort()
            
            for workout_datetime in workout_dates:
                # Choose workout type
                workout_type = random.choice(list(workout_types.keys()))
                type_config = workout_types[workout_type]
                
                # Generate workout duration and calories
                duration = random.randint(*type_config['duration_range'])
                calories = random.randint(*type_config['calories_range'])
                
                # Calculate end time
                end_datetime = workout_datetime + timedelta(minutes=duration)
                
                # Insert workout - explicitly exclude workout_id to let AUTOINCREMENT work
                workout_cursor = conn.execute(
                    'INSERT INTO Workouts (user_id, workout_type, start_time, end_time, duration_min, calories_burned) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id, workout_type, workout_datetime.strftime('%Y-%m-%d %H:%M:%S'), 
                     end_datetime.strftime('%Y-%m-%d %H:%M:%S'), duration, calories)
                )
                
                # Get the auto-generated workout_id using lastrowid
                workout_id = workout_cursor.lastrowid
                
                if not workout_id:
                    # Alternative method: use the ROWID
                    conn.execute('BEGIN IMMEDIATE')
                    result = conn.execute('SELECT last_insert_rowid()').fetchone()
                    workout_id = result[0] if result else None
                    
                if not workout_id:
                    # Final fallback: query for the most recent workout for this user
                    result = conn.execute(
                        'SELECT workout_id FROM Workouts WHERE user_id = ? ORDER BY ROWID DESC LIMIT 1', 
                        (user_id,)
                    ).fetchone()
                    workout_id = result[0] if result else None
                
                print(f"DEBUG: Created workout ID {workout_id} for user {user_id} on {workout_datetime.strftime('%Y-%m-%d %H:%M')}")
                
                if workout_id:
                    # Generate 3-8 exercises for this workout
                    num_exercises = random.randint(3, 8)
                    selected_exercises = random.sample(type_config['exercises'], min(num_exercises, len(type_config['exercises'])))
                    
                    for exercise_config in selected_exercises:
                        sets = random.randint(*exercise_config['sets_range'])
                        
                        if exercise_config['type'] == 'reps':
                            reps = random.randint(*exercise_config['reps_range'])
                        else:  # time-based
                            # Store time in minutes, convert to reps field for display
                            time_minutes = random.uniform(*exercise_config['time_range'])
                            # Convert minutes to seconds for reps field (for display purposes)
                            reps = int(time_minutes * 60)  # Store as seconds in reps field
                        
                        weight = random.uniform(*exercise_config['weight_range']) if exercise_config['weight_range'][1] > 0 else 0
                        
                        # Add some variety in notes
                        notes_options = ['', '', '', 'Great form today!', 'Felt strong', 'Challenging set', 'Good pump', 'Easy weight']
                        notes = random.choice(notes_options)
                        
                        # Insert exercise with proper workout_id
                        conn.execute(
                            'INSERT INTO Exercises (workout_id, exercise_name, sets, reps, weight_kg, notes) VALUES (?, ?, ?, ?, ?, ?)',
                            (workout_id, exercise_config['name'], sets, reps, round(weight, 1) if weight > 0 else 0, notes)
                        )
                else:
                    print(f"ERROR: Failed to get workout_id for user {user_id}")
        
        conn.commit()
        
        # Get statistics for verification
        total_workouts = conn.execute('SELECT COUNT(*) FROM Workouts').fetchone()[0]
        total_exercises = conn.execute('SELECT COUNT(*) FROM Exercises').fetchone()[0]
        
        # Verify workout IDs are properly generated
        workout_id_stats = conn.execute('SELECT MIN(workout_id), MAX(workout_id), COUNT(DISTINCT workout_id) FROM Workouts').fetchone()
        
        # Check for NULL workout_ids
        null_workouts = conn.execute('SELECT COUNT(*) FROM Workouts WHERE workout_id IS NULL').fetchone()[0]
        
        # Sample verification with workout_id and end_time from September-October 2025
        sample_workouts = conn.execute('''
            SELECT w.workout_id, w.user_id, w.workout_type, w.start_time, w.end_time, w.duration_min, COUNT(e.exercise_id) as exercise_count
            FROM Workouts w
            LEFT JOIN Exercises e ON w.workout_id = e.workout_id
            WHERE w.user_id <= 3 AND w.workout_id IS NOT NULL
            GROUP BY w.workout_id
            ORDER BY w.start_time DESC
            LIMIT 8
        ''').fetchall()
        
        verification_text = "<h3>Sample Workouts (Sep-Oct 2025):</h3>"
        for workout in sample_workouts:
            start_time = datetime.strptime(workout['start_time'], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %I:%M %p')
            end_time = datetime.strptime(workout['end_time'], '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
            verification_text += f"<p>• ID #{workout['workout_id']} (User {workout['user_id']}): {workout['workout_type'].title()} - {start_time} to {end_time} ({workout['duration_min']} min, {workout['exercise_count']} exercises)</p>"
        
        # Sample exercises by type
        verification_text += "<h3>Sample Exercises by Type:</h3>"
        for workout_type in list(workout_types.keys())[:3]:  # Show first 3 types
            sample_exercises = conn.execute('''
                SELECT e.exercise_name, e.sets, e.reps, e.weight_kg
                FROM Exercises e
                JOIN Workouts w ON e.workout_id = w.workout_id
                WHERE w.workout_type = ? AND w.workout_id IS NOT NULL
                LIMIT 3
            ''', (workout_type,)).fetchall()
            
            verification_text += f"<p><strong>{workout_type.title()}:</strong></p><ul>"
            for ex in sample_exercises:
                # Convert weight_kg to float for comparison
                try:
                    weight_kg = float(ex['weight_kg']) if ex['weight_kg'] else 0.0
                except (ValueError, TypeError):
                    weight_kg = 0.0
                
                if ex['exercise_name'] in ['Treadmill Running', 'Cycling', 'Elliptical', 'Rowing Machine', 'Stair Climber'] or 'plank' in ex['exercise_name'].lower():
                    # Time-based exercise
                    try:
                        reps = int(ex['reps']) if ex['reps'] else 0
                    except (ValueError, TypeError):
                        reps = 0
                    time_display = f"{reps//60}:{reps%60:02d}" if reps >= 60 else f"{reps}s"
                    verification_text += f"<li>{ex['exercise_name']}: {ex['sets']} sets × {time_display}</li>"
                else:
                    # Rep-based exercise
                    weight_display = f" @ {weight_kg}kg" if weight_kg > 0 else ""
                    verification_text += f"<li>{ex['exercise_name']}: {ex['sets']} sets × {ex['reps']} reps{weight_display}</li>"
            verification_text += "</ul>"
        
        # Date range verification
        date_range = conn.execute('SELECT MIN(DATE(start_time)), MAX(DATE(start_time)) FROM Workouts').fetchone()
        
        return f"""
        <h1>Success!</h1>
        <p>Generated {total_workouts} workouts with {total_exercises} exercises across 7 workout types.</p>
        <p><strong>Workout IDs:</strong> {workout_id_stats[0]} to {workout_id_stats[1]} ({workout_id_stats[2]} unique IDs)</p>
        <p><strong>Date Range:</strong> {date_range[0]} to {date_range[1]}</p>
        <p><strong>NULL workout_ids:</strong> {null_workouts}</p>
        <p><strong>Workout Types:</strong> Strength, Cardio, Flexibility, HIIT, Functional, Core</p>
        {verification_text}
        <p><a href='/dashboard'>View Dashboard</a> | <a href='/progress'>View Progress</a></p>
        """
        
    except Exception as e:
        conn.rollback()
        return f"<h1>Error:</h1><p>{str(e)}</p><p>Traceback: {traceback.format_exc()}</p>"
    
    finally:
        conn.close()

# Add a template filter for better goal progress calculation
@app.template_filter('goal_progress')
def goal_progress_filter(goal):
    """Calculate progress percentage based on goal type and direction"""
    # Handle both dict and sqlite3.Row objects
    target_value = goal['target_value'] if 'target_value' in goal else None
    if not target_value or target_value == 0:
        return 0
    
    current = goal['current_value'] if 'current_value' in goal else 0
    target = target_value
    direction = goal['goal_direction'] if 'goal_direction' in goal else 'up'
    
    if direction == 'down':
        # For goals where lower is better (weight loss, running time, etc.)
        if current <= target:
            return 100  # Goal achieved
        else:
            # Calculate progress based on how much we've improved
            # For weight loss: current=75, target=70, so we need to lose 5 more
            # Assume we started at current + 50% as starting point for calculation
            start_estimate = current + (current - target) * 0.5
            if start_estimate <= target:
                return 0
            
            progress = ((start_estimate - current) / (start_estimate - target)) * 100
            return max(0, min(100, progress))
    else:
        # For goals where higher is better (weight lifted, distance, reps, etc.)
        if current >= target:
            return 100  # Goal achieved
        else:
            return min(100, (current / target) * 100)

@app.template_filter('goal_display_text')
def goal_display_text_filter(goal):
    """Generate appropriate display text based on goal type and direction"""
    # Handle both dict and sqlite3.Row objects
    target_value = goal['target_value'] if 'target_value' in goal else None
    if not target_value:
        return "No target set"
    
    current = goal['current_value'] if 'current_value' in goal else 0
    target = target_value
    direction = goal['goal_direction'] if 'goal_direction' in goal else 'up'
    goal_type = goal['goal_type'] if 'goal_type' in goal else ''
    goal_name = goal['goal_name'] if 'goal_name' in goal else ''
    goal_name = goal_name.lower()
    
    # Debug: Let's see what we're working with
    print(f"DEBUG: Goal '{goal_name}' - current: {current}, target: {target}, direction: {direction}")
    
    if direction == 'down':
        # For "down" goals, we want current to be LOWER than target
        if current < target:
            return "Goal Achieved! 🎉"
        else:
            remaining = current - target
            # Determine unit based on goal type and name
            if 'weight' in goal_type or 'kg' in goal_name:
                return f"{remaining:.1f}kg to go"
            elif 'minutes' in goal_name or 'min' in goal_name or 'time' in goal_name:
                return f"{remaining:.1f}min faster needed"
            elif '%' in goal_name or 'percent' in goal_name or 'fat' in goal_name:
                return f"{remaining:.1f}% to reduce"
            else:
                return f"{remaining:.1f} to go"
    else:
        # For "up" goals, we want current to be HIGHER than target
        if current >= target:
            return "Goal Achieved! 🎉"
        else:
            progress = min(100, (current / target) * 100) if target > 0 else 0
            return f"{progress:.1f}% Complete"

@app.route('/workout-details/<int:workout_id>')
def workout_details(workout_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user_id = session['user_id']
    
    # Get workout details
    workout = conn.execute(
        'SELECT * FROM Workouts WHERE workout_id = ? AND user_id = ?',
        (workout_id, user_id)
    ).fetchone()
    
    if not workout:
        conn.close()
        return redirect(url_for('dashboard'))
    
    # Convert workout to dictionary and parse datetime
    workout_dict = dict(workout)
    if workout_dict['start_time']:
        try:
            from datetime import datetime
            workout_dict['start_time'] = datetime.strptime(workout_dict['start_time'], '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            workout_dict['start_time'] = None
    
    # Ensure numeric fields are properly typed
    workout_dict['duration_min'] = int(workout_dict['duration_min']) if workout_dict['duration_min'] else 0
    workout_dict['calories_burned'] = int(workout_dict['calories_burned']) if workout_dict['calories_burned'] else 0
    
    # Get exercises for this workout
    exercises = []
    try:
        exercises_raw = conn.execute(
            'SELECT * FROM Exercises WHERE workout_id = ? ORDER BY exercise_id',
            (workout_id,)
        ).fetchall()
        exercises = [dict(exercise) for exercise in exercises_raw]
        
        # Ensure numeric fields are properly typed for exercises
        for exercise in exercises:
            exercise['sets'] = int(exercise['sets']) if exercise['sets'] else 0
            exercise['reps'] = int(exercise['reps']) if exercise['reps'] else 0
            exercise['weight_kg'] = float(exercise['weight_kg']) if exercise['weight_kg'] else 0.0
            
    except sqlite3.OperationalError:
        # Exercises table might not exist
        exercises = []
    
    conn.close()
    
    return render_template('workout-details.html', workout=workout_dict, exercises=exercises)

@app.route('/delete-workout/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout and all associated exercises"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in. Please log in and try again.'}), 401
    
    conn = get_db_connection()
    user_id = session['user_id']
    
    print(f"DEBUG: Delete request - user_id from session: {user_id}, workout_id: {workout_id}")
    
    try:
        # Verify the workout exists and belongs to the current user
        workout = conn.execute(
            'SELECT workout_id, user_id FROM Workouts WHERE workout_id = ?', 
            (workout_id,)
        ).fetchone()
        
        print(f"DEBUG: Found workout: {dict(workout) if workout else 'None'}")
        
        if not workout:
            return jsonify({
                'success': False, 
                'message': 'Workout not found. It may have already been deleted.'
            }), 404
        
        # Convert to proper types for comparison
        workout_user_id = int(workout['user_id'])
        session_user_id = int(user_id)
        
        print(f"DEBUG: Comparing user IDs - workout belongs to: {workout_user_id}, session user: {session_user_id}")
        
        # Security check: ensure the workout belongs to the current user
        if workout_user_id != session_user_id:
            print(f"DEBUG: Authorization failed - workout user {workout_user_id} != session user {session_user_id}")
            return jsonify({
                'success': False, 
                'message': f'Unauthorized access. Workout belongs to user {workout_user_id} but session is user {session_user_id}.'
            }), 403
        
        # Get exercise count before deletion for confirmation message
        exercise_count_result = conn.execute(
            'SELECT COUNT(*) as count FROM Exercises WHERE workout_id = ?', 
            (workout_id,)
        ).fetchone()
        
        exercise_count = exercise_count_result['count'] if exercise_count_result else 0
        print(f"DEBUG: Found {exercise_count} exercises for workout {workout_id}")
        
        # Delete related exercises first (foreign key constraint)
        exercises_deleted = conn.execute('DELETE FROM Exercises WHERE workout_id = ?', (workout_id,))
        print(f"DEBUG: Deleted {exercises_deleted.rowcount} exercises")
        
        # Delete the workout
        workout_deleted = conn.execute('DELETE FROM Workouts WHERE workout_id = ?', (workout_id,))
        print(f"DEBUG: Deleted {workout_deleted.rowcount} workouts")
        
        # Commit the transaction
        conn.commit()
        print(f"DEBUG: Transaction committed successfully")
        
        # Return success response
        message = 'Workout deleted successfully!'
        if exercise_count > 0:
            message += f' Removed {exercise_count} exercise record{"s" if exercise_count != 1 else ""}.'
        
        return jsonify({
            'success': True, 
            'message': message
        })
        
    except sqlite3.Error as e:
        # Rollback in case of database error
        conn.rollback()
        print(f"Database error deleting workout {workout_id}: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Database error: {str(e)}'
        }), 500
        
    except Exception as e:
        # Handle any other unexpected errors
        conn.rollback()
        print(f"Unexpected error deleting workout {workout_id}: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False, 
            'message': f'Unexpected error: {str(e)}'
        }), 500
        
    finally:
        conn.close()

@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/serviceworker.js')
def serviceworker():
    return send_from_directory('.', 'serviceworker.js')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
