import sqlite3
import db

conn = sqlite3.connect('models/planner.db')

# db.add_user('dpfinest', 'Daniel Park', 'danielpark@gmail.com', 'backboardhitter' )

# db.add_task('danielpark@gmail.com', 'visit apartment in VA', 'Still looking for a place to live and reston and tyson VA is the option.')

# db.add_goal('kwapong91@gmail.com', 'ai project', 'Learning python while building something that is related to ai')

# db.fetch_user('kwapong91@gmail.com')

db.fetch_goals('kwapong91@gmail.com')