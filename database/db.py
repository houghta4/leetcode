import sqlite3 as sql

DB_PATH = 'database/leetcode_bot.db'


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.connection = sql.connect(self.db_path)
        self.connection.row_factory = sql.Row
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
    
    def execute(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        return self.cursor

    def add_user(self, discord_id, discord_username: str = None, leetcode_username: str = None):
        self.execute('INSERT OR IGNORE INTO users (discord_id, discord_username, leetcode_username, score) VALUES (?, ?, ?, ?)', (discord_id, discord_username, leetcode_username, 0))
        self.commit()
    
    def get_user(self, discord_id):
        self.execute('SELECT * FROM users WHERE discord_id = ? ', (discord_id,))
        return self.cursor.fetchone()

    def get_discord_username(self, discord_id):
        cursor = self.execute('SELECT discord_username FROM users WHERE discord_id = ?', (discord_id,))
        res = cursor.fetchone()
        return res[0] if res else [-1]
    
    def set_discord_username(self, discord_id, username):
        self.execute('UPDATE users SET discord_username = ? WHERE discord_id = ?', (username, discord_id))
        self.commit()
    
    def get_score(self, discord_id):
        cursor = self.execute('SELECT score FROM users WHERE discord_id = ?', (discord_id,))
        res = cursor.fetchone()
        return res[0] if res else -1
    
    def update_score(self, discord_id, amount):
        self.execute('UPDATE users SET score = score + ? WHERE discord_id = ?', (amount, discord_id))
        self.commit()

    def get_leetcode_username(self, discord_id):
        cursor = self.execute('SELECT leetcode_username FROM users WHERE discord_id = ?', (discord_id,))
        res = cursor.fetchone()
        return res[0] if res else f'Error getting leetcode username from {discord_id}'
    
    def set_leetcode_username(self, discord_id, username):
        self.execute('UPDATE users SET leetcode_username = ? WHERE discord_id = ?', (username, discord_id))
        self.commit()

    def get_all_users(self):
        self.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_columns(self, table):
        query = f'SELECT * FROM {table} LIMIT 1'
        self.cursor.execute(query)
        col_names = [desc[0] for desc in self.cursor.description]
        return col_names

    def get_all_table(self, table):
        query = f'SELECT * FROM {table}'
        self.execute(query)
        return self.cursor.fetchall()
