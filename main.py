from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db_connection():
    conn = sqlite3.connect('database/data_source.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
            session['name'] = user['name'] if 'name' in user else 'User'
            # Fallback to 'User' if 'name' is missing
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user_data = conn.execute(
        'SELECT first_name, surname, email FROM Users WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()
    workouts = conn.execute(
        'SELECT workout_type, duration_min, calories_burned, start_time '
        'FROM Workouts WHERE user_id = ? ORDER BY start_time DESC LIMIT 5',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('dashboard.html', user=user_data, workouts=workouts)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user_data = conn.execute(
        'SELECT first_name, surname, email, age, height_cm, weight_kg '
        'FROM Users WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')
        conn.execute(
            'UPDATE Users SET first_name = ?, surname = ?, email = ?, '
            'age = ?, height_cm = ?, weight_kg = ? WHERE user_id = ?',
            (
                first_name, surname, email,
                age, height, weight, session['user_id']
            )
        )
        conn.commit()
        conn.close()
        session['name'] = f"{first_name} {surname}"
        return redirect(url_for('profile'))
    conn.close()
    return render_template('profile.html', user=user_data)


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/log-workout', methods=['GET', 'POST'])
def log_workout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    if request.method == 'POST':
        workout_type = request.form.get('workout_type')
        duration = request.form.get('duration')
        calories = request.form.get('calories')
        conn.execute(
            'INSERT INTO Workouts '
            '(user_id, workout_type, duration_min, calories_burned) '
            'VALUES (?, ?, ?, ?)',
            (session['user_id'], workout_type, duration, calories)
        )
        conn.commit()
    workouts = conn.execute(
        'SELECT * FROM Workouts WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('log-workout.html', workouts=workouts)


@app.route('/progress', methods=['GET'])
def progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    progress_data = conn.execute(
        'SELECT DATE(start_time) AS workout_date, '
        'SUM(duration_min) AS total_minutes, '
        'SUM(calories_burned) AS total_calories '
        'FROM Workouts WHERE user_id = ? '
        'GROUP BY workout_date '
        'ORDER BY workout_date ASC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('progress.html', progress_data=progress_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
