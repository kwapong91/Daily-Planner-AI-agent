import sqlite3

conn = sqlite3.connect('planner.db')  
cursor = conn.cursor()

# Add a new user
def add_user(name, email, password):
    cursor.execute(
        f"INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)"
    )
    conn.commit
# Add a new goal
def add_goal(email, title, description):
    user_id = cursor.execute(
        f"""
            SELECT user_id
            FROM users
            WHERE email = "{email}"
        """
    )
    cursor.execute(
        f"INSERT INTO users (user_id, title, description) VALUES (?, ?, ?)"
    )
# Add a new task
def add_task(email, title, status):
    goal_id = cursor.execute(
        f"""
            SELECT goal_id
            FROM goals
            WHERE user_id = (
                SELECT user_id
                FROM users
                WHERE email = "?"
            );
        """
    )
    cursor.execute(
       f"INSERT INTO tasks (goal_id, title, status) VALUES (?, ?, ?)"
    )
# Fetch user by ID or email
def fetch_user(email, user_id):
    cursor.execute(
        f"""
        SELECT username
        FROM users
        WHERE email = "?" or user_id = ?
         """
    )
# Fetch goals for a user
def fetch_goals(user_id):
    cursor.execute(
        f"""
        SELECT title
        FROM goals
        WHERE user_id = "?"
        """
    )

# Fetch all task for a goal
def fetch_task_for_goal(email):
    cursor.execute(
        """
        SELECT t.title, t.goal_id
        FROM tasks t
        JOIN goals g ON t.goal_id = g.goal_id
        JOIN users u ON g.user_id = u.user_id
        WHERE u.email = ?
        """,
        (email,)
    )

# Update the status of a task
def update_task_status(task_id, new_status, email):
    cursor.execute(
        """
        UPDATE tasks
        SET status = ?
        WHERE task_id = ?
        AND goal_id IN (
            SELECT g.goal_id
            FROM goals g
            JOIN users u ON g.user_id = u.user_id
            WHERE u.email = ?
        )
        """,
        (new_status, task_id, email)
    )
    conn.commit()
