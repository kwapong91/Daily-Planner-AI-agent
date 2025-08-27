import sqlite3

conn = sqlite3.connect('planner.db')  
cursor = conn.cursor()

table_creation_query = """
    CREATE TABLE tasks (
        task_id INTEGER PRIMARY KEY, 
        goal_id NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL default 'pending',
        due_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (goal_id) REFERENCES goals(goal_id)
    )
"""
try:
    cursor.execute(table_creation_query)
except sqlite3.OperationalError as e:
    print(f"Operational error: {e}")
except sqlite3.IntegrityError as e:
    print(f"Integrity error: {e}")
except sqlite3.Error as e:
    print(f"Database error: {e}")
else:
    print("Table is ready!")
finally:
    cursor.close()

# Made changes to primary key by making it not null