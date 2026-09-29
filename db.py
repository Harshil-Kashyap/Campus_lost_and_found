import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / 'data' / 'lost_found.db'


def get_db():
    DB_FILE.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def setup_db():
    db = get_db()
    db.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        pwd TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student'
    );
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        kind TEXT NOT NULL CHECK(kind IN ('lost','found')),
        title TEXT NOT NULL,
        cat TEXT NOT NULL,
        place TEXT NOT NULL,
        day TEXT NOT NULL,
        info TEXT,
        status TEXT NOT NULL DEFAULT 'open',
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        note TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(item_id, user_id),
        FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    ''')
    add_user(db, 'Demo Student', 'student@campus.local', 'student123', 'student')
    add_user(db, 'Campus Admin', 'admin@campus.local', 'admin123', 'admin')
    db.commit()
    db.close()


def add_user(db, name, email, pwd, role='student'):
    import hashlib
    hp = hashlib.sha256(pwd.encode()).hexdigest()
    db.execute('INSERT OR IGNORE INTO users(name,email,pwd,role) VALUES(?,?,?,?)',
               (name, email.lower().strip(), hp, role))
