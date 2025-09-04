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
        added_goal_message = f"New goal has been added: {title}"
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
            print(added_goal_message)
        else:
            print("New goal was unable to be added")

   






# Add a new task
def add_task(email, title, description):
    conn = sqlite3.connect('models/planner.db')
    cursor = conn.cursor()
    success_message = None

    try:

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
            print('There was an error with retrieving this accounts goals.')
            return
        goal_id = result[0]

        cursor.execute(
        "INSERT INTO tasks (goal_id, title, description) VALUES (?, ?, ?)",
        (goal_id, title, description)
        )

        conn.commit()
        success_message = f"The following task was added: {title}"

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
        if success_message:
            print(success_message)
        else:
            print("New task was unable to be added")


# Fetch user by ID or email
def fetch_user(email):
    conn = sqlite3.connect('models/planner.db')
    cursor = conn.cursor()
    success_message = None
    result = None
    
    try:
            
        cursor.execute(
            """
            SELECT username
            FROM users
            WHERE email = ?
            """,
            (email,)
        )
        
        result = cursor.fetchone()
        if result is None:
            print('There was an error getting the user information with the email')
            return
        
        success_message = f"Here is the users  email: {result[0]}"
        return result[0]
    
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
        if success_message:
            print(success_message)
        else:
            print("Fetch was unsuccessful")


# Fetch goals for a user
def fetch_goals(email):
    conn = sqlite3.connect('models/planner.db')
    cursor = conn.cursor()
    success_message = None
    result = None

    try:
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE email = ?
            """,
            (email,)
        )
        result = cursor.fetchone()

        if result is None:
            print("Unable to find user")
            return
        user_id = result[0]
            
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
    
        success_message = f"Here is the users  goal: {result[0]}"
        return result[0]
    
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
        if success_message:
            print(success_message)
        else:
            print("Fetch was unsuccessful")

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
    result = cursor.fetchmany()
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
