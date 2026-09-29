from db import get_db


def stats():
    db = get_db()
    out = {}
    for name, sql in {
        'lost': "SELECT COUNT(*) FROM items WHERE kind='lost'",
        'found': "SELECT COUNT(*) FROM items WHERE kind='found'",
        'open': "SELECT COUNT(*) FROM items WHERE status='open'",
        'returned': "SELECT COUNT(*) FROM items WHERE status='returned'",
        'claims': "SELECT COUNT(*) FROM claims WHERE status='pending'",
        'users': 'SELECT COUNT(*) FROM users'
    }.items():
        out[name] = db.execute(sql).fetchone()[0]
    db.close()
    return out
