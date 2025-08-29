# db.py Documentation

## **File Purpose**
`db.py` acts as the **data layer** for the AI Planner backend. It handles all interactions with the SQLite database (`planner.db`) and provides helper functions for creating and retrieving users, goals, and tasks.

---

## **Database Connection**
- Uses SQLite (`sqlite3`) with the file `planner.db`.  
- The connection and cursor are created at the top of the file:
```python
conn = sqlite3.connect('planner.db')
cursor = conn.cursor()
