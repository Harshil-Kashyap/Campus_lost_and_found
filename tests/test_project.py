import os
import tempfile
import unittest
from unittest.mock import patch

class TestProject(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        patcher = patch('db.DB_FILE', __import__('pathlib').Path(self.tmp.name))
        self.patcher = patcher
        patcher.start()
        import db
        db.setup_db()

    def tearDown(self):
        self.patcher.stop()
        os.unlink(self.tmp.name)

    def test_register_and_login(self):
        from auth import register, login
        ok, _ = register('Aman', 'aman@test.com', 'abc123')
        self.assertTrue(ok)
        self.assertEqual(login('aman@test.com', 'abc123')['name'], 'Aman')
        self.assertIsNone(login('aman@test.com', 'wrong'))

    def test_item_search(self):
        from items import add_item, get_items
        add_item(1, 'lost', 'Black Wallet', 'Wallet', 'Library', '28-09-2026', 'Small black wallet')
        rows = get_items('lost', 'wallet')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['title'], 'Black Wallet')

    def test_claim_and_approval(self):
        from items import add_item
        from claims import add_claim, get_claims, set_claim
        iid = add_item(1, 'found', 'Blue Bottle', 'Bottle', 'Canteen', '28-09-2026', 'Blue bottle')
        ok, _ = add_claim(iid, 1, 'It has my name sticker.')
        self.assertTrue(ok)
        rows = get_claims(1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['status'], 'pending')
        self.assertTrue(set_claim(rows[0]['id'], 'approved'))
        self.assertEqual(get_claims(1)[0]['status'], 'approved')

    def test_stats(self):
        from reports import stats
        s = stats()
        self.assertEqual(s['users'], 2)
        self.assertEqual(s['lost'], 0)
        self.assertEqual(s['found'], 0)

if __name__ == '__main__':
    unittest.main()
