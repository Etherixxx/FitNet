from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_secret_key'


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

    if request.method == 'POST':
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
        conn.close()

        # Update the session name
        session['name'] = f"{first_name} {surname}"
        return redirect(url_for('profile'))

    user_data = conn.execute(
        "SELECT Users.*, Progress.height_cm, Progress.weight_kg FROM Users "
        "LEFT JOIN Progress ON Users.user_id = Progress.user_id "
        "WHERE Users.user_id = ?",
        (user_id,)
    ).fetchone()

    conn.close()
    return render_template('profile.html', user_data=user_data)


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


@app.route('/progress', methods=['GET'])
def progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user_id = session['user_id']
    
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

    # Get weekly workout data for chart
    weekly_data = conn.execute(
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

    # Get strength progress data (example with bench press)
    strength_data = conn.execute(
        '''SELECT DATE(w.start_time) as workout_date, MAX(e.weight_kg) as max_weight
        FROM Workouts w
        JOIN Exercises e ON w.workout_id = e.workout_id
        WHERE w.user_id = ? AND e.exercise_name LIKE '%bench%press%'
        GROUP BY DATE(w.start_time)
        ORDER BY DATE(w.start_time)''',
        (user_id,)
    ).fetchall()

    # Get monthly overview data
    monthly_data = conn.execute(
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

    conn.close()
    
    return render_template('progress.html', 
                         progress_data=progress_data,
                         total_workouts=total_workouts,
                         total_time=total_time,
                         avg_duration=avg_duration,
                         weekly_data=weekly_data,
                         strength_data=strength_data,
                         monthly_data=monthly_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
