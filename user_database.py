#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3

class UserDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username text UNIQUE,
            password text,
            watchlist text DEFAULT ''
        )"""
        self.c.execute(query)
        self.conn.commit()

    def create_user(self, username, password):
        try:
            self.c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username):
        self.c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.c.fetchone()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "password": user[2],
                "watchlist": user[3]
            }
        else:
            return None

    def update_watchlist(self, username, watchlist):
        watchlist_str = ",".join(watchlist)
        self.c.execute("UPDATE users SET watchlist = ? WHERE username = ?", (watchlist_str, username))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

