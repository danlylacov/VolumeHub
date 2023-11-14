import sqlite3
from dotenv.main import load_dotenv
import os


class UsersDataBase:

    def __init__(self):
        self.db = sqlite3.connect('admin.db')
        self.cur = self.db.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            userid INTEGER,
                            username TEXT,
                            subscription TEXT)
                            """)
        self.db.commit()


    def add_user(self, userid, username):
        self.cur.execute('INSERT INTO users(userid, username, subscription) VALUES (?, ?, "-");', (userid, username))
        self.db.commit()


    def get_userids(self):
        result = []
        userids = self.cur.execute('SELECT userid FROM users')
        for el in userids:
            result.append(el[0])
        return result


    def give_subscription_to_user(self, interval):
        self.cur.execute()

    def get_Z(self):
        return float(self.cur.execute("""SELECT value FROM settings WHERE name = "Z_deviation";""").fetchone()[0])


    def update_Z(self, z):
        self.cur.execute(f'UPDATE settings SET value = {z} WHERE name = "Z_deviation";')
        self.db.commit()


    def get_about_bot_text(self):
        return str(self.cur.execute("""SELECT value FROM settings WHERE name = "about_bot_text";""").fetchone()[0])

    def update_about_bot_text(self, about: str):
        self.cur.execute(f'UPDATE settings SET value = "{about}" WHERE name = "about_bot_text";')
        self.db.commit()


    def get_prices(self):
        days30 = self.cur.execute("""SELECT value FROM settings WHERE name = "30_days";""").fetchone()[0]
        days90 = self.cur.execute("""SELECT value FROM settings WHERE name = "90_days";""").fetchone()[0]
        days365 = self.cur.execute("""SELECT value FROM settings WHERE name = "365_days";""").fetchone()[0]
        return [days30, days90, days365]


    def update_prices(self, days30, days90, days365):
        self.cur.execute(f'UPDATE settings SET value = "{days30}" WHERE name = "30_days";')
        self.cur.execute(f'UPDATE settings SET value = "{days90}" WHERE name = "90_days";')
        self.cur.execute(f'UPDATE settings SET value = "{days365}" WHERE name = "365_days";')
        self.db.commit()


    def get_subscription_text(self):
        return str(self.cur.execute("""SELECT value FROM settings WHERE name = "subscription_text";""").fetchone()[0])


    def update_subscription_text(self, text):
        self.cur.execute(f'UPDATE settings SET value = "{text}" WHERE name = "subscription_text";')
        self.db.commit()




