import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy
from src.api import create_app
from src.database.models import setup_db, db_drop_and_create_all, Drink, database_filename, database_path, project_dir


class CoffeeShopAPITestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['drinks']) >= 0)
        self.assertTrue(data['success'])

    def test_get_drinks_details(self):
        res = self.client().get('/drinks-detail')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_drinks(self):
        res = self.client().post('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_patch_drinks(self):
        res = self.client().patch('/drinks/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_drinks(self):
        res = self.client().patch('/drinks/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
