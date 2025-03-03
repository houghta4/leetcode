import sqlite3

DB_PATH = 'database/leetcode_bot.db'

con = sqlite3.connect(DB_PATH)
cursor = con.cursor()

cursor.execute('DROP TABLE IF EXISTS users')

con.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_id INTEGER UNIQUE,
    discord_username STRING DEFAULT "",
    leetcode_username STRING DEFAULT "",
    score INTEGER DEFAULT 0         
)
''')

con.commit()
con.close()

print('leetcode_bot.db initialized')