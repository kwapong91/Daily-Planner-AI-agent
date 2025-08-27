import sqlite3

conn = sqlite3.connect('planner.db')  
cursor = conn.cursor()

# Add a new user
def add_user(name, email, password):
    cursor.execute(
        f"INSERT INTO users (name, email, password_hash) VALUE ({name}, {email}, {password})"
    )
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
        f"INSERT INTO users (user_id, title, description) VALUE ({user_id}, {title}, {description})"
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
                WHERE email = "{email}"
            );
        """
    )
    cursor.execute(
       f"INSERT INTO tasks (goal_id, title, status) VALUE ({goal_id}, {title}, {status})"
    )
# Fetch user by ID or email
def fetch_user(email, user_id):
    cursor.execute(
        f"""
            SELECT username
            FROM users
            WHERE email = "{email}" or user_id = {user_id}
         """
    )
# Fetch goals for a user

# Fetch all task for a goal

# Update the status of a task

