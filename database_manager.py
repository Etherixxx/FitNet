import sqlite3 as sql


def listExtension():
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    data = cur.execute('SELECT * FROM Users').fetchall()
    con.close()
    return data


def fetch_dashboard_data():
    con = sql.connect("database/data_source.db")
    cur = con.cursor()

    # SQL queries
    recent_workouts_query = (
        "SELECT workout_type, start_time, duration_min, calories_burned "
        "FROM Workouts "
        "ORDER BY start_time DESC LIMIT 3"
    )
    weekly_workouts_query = (
        "SELECT COUNT(*) "
        "FROM Workouts "
        "WHERE start_time >= date('now', '-7 days')"
    )
    total_time_query = (
        "SELECT SUM(duration_min) "
        "FROM Workouts "
        "WHERE start_time >= date('now', '-7 days')"
    )

    # Execute queries
    recent_workouts = cur.execute(recent_workouts_query).fetchall()
    weekly_workouts = cur.execute(weekly_workouts_query).fetchone()
    total_time = cur.execute(total_time_query).fetchone()

    con.close()

    return {
        "recent_workouts": recent_workouts,
        "weekly_workouts": weekly_workouts[0] if weekly_workouts else 0,
        "total_time": total_time[0] if total_time else 0,
    }
