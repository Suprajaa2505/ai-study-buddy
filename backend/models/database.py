import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'studybuddy.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY, filename TEXT, original_filename TEXT,
        created_at TEXT, page_count INTEGER, file_size INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT,
        role TEXT, content TEXT, created_at TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE)''')
    conn.commit(); conn.close()

def create_session(session_id, filename, original_filename, page_count=0, file_size=0):
    conn = get_db()
    conn.execute('INSERT INTO sessions VALUES (?,?,?,?,?,?)',
        (session_id, filename, original_filename, datetime.utcnow().isoformat(), page_count, file_size))
    conn.commit(); conn.close()

def get_session(session_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM sessions WHERE id=?', (session_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_sessions():
    conn = get_db()
    rows = conn.execute('SELECT * FROM sessions ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_session(session_id):
    conn = get_db()
    conn.execute('DELETE FROM sessions WHERE id=?', (session_id,))
    conn.commit(); conn.close()

def save_message(session_id, role, content):
    conn = get_db()
    conn.execute('INSERT INTO messages (session_id,role,content,created_at) VALUES (?,?,?,?)',
        (session_id, role, content, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()

def get_messages(session_id):
    conn = get_db()
    rows = conn.execute('SELECT * FROM messages WHERE session_id=? ORDER BY created_at ASC', (session_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]