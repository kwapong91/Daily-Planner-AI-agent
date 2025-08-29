import sqlite3
import db

conn = sqlite3.connect('models/planner.db')

db.add_user('dpfinest', 'Daniel Park', 'danielpark@gmail.com', 'backboardhitter' )

db.add_goal('danielpark@gmail.com', 'Buying Apartment', 'Trying to get a apartment in VA by mid september')