import sqlite3

conn = sqlite3.connect('planner.db')  
cursor = conn.cursor()

table_creation_query = """
    CREATE TABLE goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL DEFAULT "pending",
        FOREIGN KEY (user_id) REFERENCES users(user_id)
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
