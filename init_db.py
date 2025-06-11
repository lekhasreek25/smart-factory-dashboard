import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL
)
''')

conn.commit()
conn.close()

print("✅ Database initialized.")
