import sqlite3

conn = sqlite3.connect('models/planner.db')  
cursor = conn.cursor()

# Add a new user
def add_user(username, name, email, password):
    conn = sqlite3.connect('models/planner.db')  
    cursor = conn.cursor()
    added_user_message = None
    try: 
        cursor.execute(
        "INSERT INTO users (username, name, email, password_hash) VALUES (?, ?, ?, ?)",
        (username, name, email, password)
        )
        conn.commit()
        added_user_message = f"{name} has been added to the database."   
    except sqlite3.OperationalError as e:
        print(f"Operational error: {e}")
        return
    except Exception as e:
        print(f"An error has occurred trying to add a new user:{e}")
        return
    finally:
        conn.close()
        if added_user_message:
            print(added_user_message)


 
# Add a new goal
def add_goal(email, title, description):
    conn = sqlite3.connect('models/planner.db')  
    cursor = conn.cursor()
    added_goal_message = None

    try:
        cursor.execute(
            """
                SELECT user_id
                FROM users
                WHERE email = ?
            """, (email,)
        )

        result = cursor.fetchone()
        if not result:
            print(f"NO user found with email: {email}")
            return
        user_id = result[0]

        cursor.execute(
        "INSERT INTO goals (user_id, title, description) VALUES (?, ?, ?)",
        (user_id, title, description)
        )
        added_goal_message = f"Added the following goal: {title}"
        conn.commit()

    except sqlite3.OperationalError as e:
        conn.rollback()
        print(f"Operational error: {e}")
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"Integrity error: {e}")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()        
        if added_goal_message:
            print(f"New goal has been added: {added_goal_message}")
        else:
            print("New goal was unable to be added")

   






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
    conn.close()


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
    conn.close()
