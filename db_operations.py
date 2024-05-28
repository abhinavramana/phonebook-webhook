import sqlite3


DATABASE_NAME = 'user_data.db'


def init_db():
    # Initialize the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        person_id TEXT PRIMARY KEY,
        current_name TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS name_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        name TEXT,
        timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()


# Utility functions for database operations
def add_person(person_id, name, timestamp):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO user_data (person_id, current_name) VALUES (?, ?)', (person_id, name))
    cursor.execute('INSERT INTO name_history (person_id, name, timestamp) VALUES (?, ?, ?)',
                   (person_id, name, timestamp))
    conn.commit()
    conn.close()


def rename_person(person_id, name, timestamp):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE user_data SET current_name = ? WHERE person_id = ?', (name, person_id))
    cursor.execute('INSERT INTO name_history (person_id, name, timestamp) VALUES (?, ?, ?)',
                   (person_id, name, timestamp))
    conn.commit()
    conn.close()


def remove_person(person_id, timestamp):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_data WHERE person_id = ?', (person_id,))
    cursor.execute('INSERT INTO name_history (person_id, name, timestamp) VALUES (?, ?, ?)',
                   (person_id, None, timestamp))
    conn.commit()
    conn.close()


def get_current_name(person_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT current_name FROM user_data WHERE person_id = ?', (person_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


def get_name_history(person_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, timestamp FROM name_history WHERE person_id = ? ORDER BY timestamp', (person_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def get_all_persons():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT person_id, current_name FROM user_data')
    result = cursor.fetchall()
    conn.close()
    return result