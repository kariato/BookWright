# bookwright/utils/database_manager.py
import sqlite3

class StoryDatabase:
    def __init__(self, db_file='story.db'):
        self.conn = sqlite3.connect(db_file)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS characters (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        appearance TEXT,
                        personality TEXT,
                        likes TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS chapters (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        outline TEXT,
                        generated_text TEXT
        )''')
        self.conn.commit()

    def add_character(self, name, description, appearance, personality, likes):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO characters (name, description, appearance, personality, likes)
                       VALUES (?, ?, ?, ?, ?)''',
                    (name, description, appearance, personality, likes))
        self.conn.commit()

    def get_characters(self):
        cur = self.conn.cursor()
        cur.execute('SELECT name, description, appearance, personality, likes FROM characters')
        return cur.fetchall()

    def add_chapter(self, title, outline, generated_text):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO chapters (title, outline, generated_text)
                       VALUES (?, ?, ?)''', (title, outline, generated_text))
        self.conn.commit()

    def close(self):
        self.conn.close()
