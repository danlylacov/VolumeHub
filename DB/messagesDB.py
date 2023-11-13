import sqlite3


class Message:


    def __init__(self):
        self.db =  self.db = sqlite3.connect('../tg_bot/dmin.db')
        self.cur = self.db.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS messages(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            message_text TEXT)""")
        self.db.commit()


    def insert_message(self, name, message):
        self.cur.execute(f'INSERT INTO messages(name, message_text) VALUES (?, ?);', (name, message, ))
        self.db.commit()

db = Message()
db.insert_message('w', 'wdwwd')