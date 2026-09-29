from db import get_db


def add_item(uid, kind, title, cat, place, day, info):
    db = get_db()
    cur = db.execute('''INSERT INTO items(user_id,kind,title,cat,place,day,info)
                        VALUES(?,?,?,?,?,?,?)''',
                     (uid, kind, title.strip(), cat.strip(), place.strip(), day.strip(), info.strip()))
    db.commit()
    iid = cur.lastrowid
    db.close()
    return iid


def get_items(kind=None, word=''):
    db = get_db()
    sql = '''SELECT items.*, users.name AS who FROM items
             JOIN users ON users.id=items.user_id WHERE 1=1'''
    vals = []
    if kind:
        sql += ' AND kind=?'
        vals.append(kind)
    word = word.strip()
    if word:
        sql += ' AND (title LIKE ? OR cat LIKE ? OR place LIKE ?)'
        vals += [f'%{word}%'] * 3
    sql += ' ORDER BY items.id DESC'
    rows = db.execute(sql, vals).fetchall()
    db.close()
    return rows


def my_items(uid):
    db = get_db()
    rows = db.execute('SELECT * FROM items WHERE user_id=? ORDER BY id DESC', (uid,)).fetchall()
    db.close()
    return rows


def close_item(iid, uid=None):
    db = get_db()
    if uid is None:
        cur = db.execute("UPDATE items SET status='returned' WHERE id=?", (iid,))
    else:
        cur = db.execute("UPDATE items SET status='returned' WHERE id=? AND user_id=?", (iid, uid))
    db.commit()
    ok = cur.rowcount > 0
    db.close()
    return ok


def delete_item(iid, uid):
    db = get_db()
    cur = db.execute('DELETE FROM items WHERE id=? AND user_id=?', (iid, uid))
    db.commit()
    ok = cur.rowcount > 0
    db.close()
    return ok
