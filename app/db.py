import sqlite3

conn = sqlite3.connect('planner.db')  
cursor = conn.cursor()

# Add a new user
def add_user(name, email, password):
    cursor.execute(
    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
    (name, email, password)
    )
    conn.commit()

# Add a new goal
def add_goal(email, title, description):
    cursor.execute(
        """
            SELECT user_id
            FROM users
            WHERE email = ?
        """, (email,)
    )
    result = cursor.fetchone() # Stores the user_id
    if result is None:
        print("No result found for user_id")
        return
    user_id = result[0]
    cursor.execute(
        "INSERT INTO goals (user_id, title, description) VALUES (?, ?, ?)",
        (user_id, title, description)
    )
    conn.commit()

# Add a new task
def add_task(email, title, status):
    cursor.execute(
        """
        SELECT goal_id
        FROM goals
        WHERE user_id = (
            SELECT user_id
            FROM users
            WHERE email = ?
            )
        """,
        (email,)
    )
    result = cursor.fetchone()
    if result is None:
        print('There was an error with retrieving the goal_id')
        return
    
    goal_id = result[0]

    cursor.execute(
       "INSERT INTO tasks (goal_id, title, status) VALUES (?, ?, ?)",
       (goal_id, title, status)
    )
    conn.commit()

# Fetch user by ID or email
def fetch_user(email, user_id):
    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE email = ? or user_id = ?
         """,
        (email, user_id)
    )
    result = cursor.fetchone()
    if result is None:
        print('There was an error getting the user with the ID or email')
        return
    return result[0]

# Fetch goals for a user
def fetch_goals(user_id):
    cursor.execute(
        """
        SELECT title
        FROM goals
        WHERE user_id = ?
        """,
        (user_id,)
    )
    result = cursor.fetchone()
    if result is None:
        print("There was an error in fetching the goal for the user using title")
        return
    return result[0]

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
    result = cursor.fetchone()
    if result is None:
        print("There was an erroing fetching the task for the goals for the user")
        return
    return result[0]

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
