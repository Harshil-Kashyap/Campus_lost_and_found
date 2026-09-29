from db import get_db


def add_claim(iid, uid, note):
    db = get_db()
    try:
        db.execute('INSERT INTO claims(item_id,user_id,note) VALUES(?,?,?)', (iid, uid, note.strip()))
        db.commit()
        return True, 'Claim submitted.'
    except Exception:
        return False, 'You have already claimed this item.'
    finally:
        db.close()


def get_claims(uid=None, admin=False):
    db = get_db()
    sql = '''SELECT claims.*, items.title, items.kind, users.name AS student
             FROM claims JOIN items ON items.id=claims.item_id
             JOIN users ON users.id=claims.user_id'''
    vals = []
    if not admin:
        sql += ' WHERE claims.user_id=?'
        vals.append(uid)
    sql += ' ORDER BY claims.id DESC'
    rows = db.execute(sql, vals).fetchall()
    db.close()
    return rows


def set_claim(cid, status):
    db = get_db()
    row = db.execute('SELECT item_id FROM claims WHERE id=?', (cid,)).fetchone()
    if not row:
        db.close()
        return False
    db.execute('UPDATE claims SET status=? WHERE id=?', (status, cid))
    if status == 'approved':
        db.execute("UPDATE items SET status='returned' WHERE id=?", (row['item_id'],))
    db.commit()
    db.close()
    return True
