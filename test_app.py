import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Candidate, Job, Company, setup_db

class FullProjectTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "dbebe2jg03i7ts"
        self.database_path = 'postgres://kqohredagknkof:594066de91704a25da1c3f88707388b80c10e47b969c2e9cfb3bc6bab4659b0c@ec2-3-208-50-226.compute-1.amazonaws.com:5432/dbebe2jg03i7ts'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_companies(self):
        res = self.client().get('/companies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['companies'], [])

if __name__ == "__main__":
    unittest.main()
