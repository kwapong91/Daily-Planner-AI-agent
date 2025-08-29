import sqlite3
# import app.db

conn = sqlite3.connect('models/planner.db')
cursor = conn.cursor()


cursor.execute(
    'SELECT * FROM goals'
)
result = cursor.fetchone()
cursor.close

print(result)