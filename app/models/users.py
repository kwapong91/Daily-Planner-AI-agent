import sqlite3

conn = sqlite3.connect('planner.db')  
cursor = conn.cursor()

table_creation_query = """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
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



