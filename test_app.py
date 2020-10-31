import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Candidate, Job, Company, setup_db

TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
TEST_DATABASE_NAME = os.environ.get('TEST_DATABASE_NAME')

DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
BAD_TOKEN = 'BAD_TOKEN'


class FullProjectTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DATABASE_NAME
        self.database_path = TEST_DATABASE_URL
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    """
        Get endpoint tests
    """

    def test_get_companies(self):
        res = self.client().get('/companies')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['companies']), list)

    def test_get_companies_error(self):
        res = self.client().get('/companies?page=-2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_jobs(self):
        res = self.client().get('/jobs')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['jobs']), list)

    def test_get_jobs_error(self):
        res = self.client().get('/jobs?page=-2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """
        Company creation tests
    """

    def test_create_company_public(self):
        company = {"name": 'Simple', "description": 'company',
                   "imageBase64": '', "state": 'Bahia', "city": 'Salvador'}
        res = self.client().post('/company', json=company)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_company_assistant(self):
        company = {"name": 'Simple', "description": 'company',
                   "imageBase64": '', "state": 'Bahia', "city": 'Salvador'}
        res = self.client().post(
            '/company',
            json=company,
            headers={
                'Authorization': ASSISTANT_TOKEN})

        data = json.loads(res.data)
        company_data = data['company']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(company_data['name'], company['name'])
        self.assertEqual(company_data['description'], company['description'])
        self.assertEqual(company_data['imageBase64'], company['imageBase64'])
        self.assertEqual(company_data['state'], company['state'])
        self.assertEqual(company_data['city'], company['city'])

    def test_create_company_director(self):
        company = {"name": 'Simple', "description": 'company',
                   "imageBase64": '', "state": 'Bahia', "city": 'Salvador'}
        res = self.client().post(
            '/company',
            json=company,
            headers={
                'Authorization': DIRECTOR_TOKEN})

        data = json.loads(res.data)
        company_data = data['company']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(company_data['name'], company['name'])
        self.assertEqual(company_data['description'], company['description'])
        self.assertEqual(company_data['imageBase64'], company['imageBase64'])
        self.assertEqual(company_data['state'], company['state'])
        self.assertEqual(company_data['city'], company['city'])

    def test_create_company_error(self):
        company = {"description": 'company',
                   "imageBase64": '', "state": 'Bahia', "city": 'Salvador'}
        res = self.client().post(
            '/company',
            json=company,
            headers={
                'Authorization': DIRECTOR_TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_company(self):
        company = {
            "description": 'company',
            "imageBase64": '',
            "state": 'Bahia',
            "city": 'Lauro de Freitas'}
        res = self.client().patch(
            '/company/3',
            json=company,
            headers={
                'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)
        company_data = data['company']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(company_data['description'], company['description'])
        self.assertEqual(company_data['imageBase64'], company['imageBase64'])
        self.assertEqual(company_data['state'], company['state'])
        self.assertEqual(company_data['city'], company['city'])

    def test_update_company_error(self):
        company = {
            "description": 'company',
            "imageBase64": '',
            "state": 'Bahia',
            "city": 'Lauro de Freitas'}
        res = self.client().patch(
            '/company/10000',
            json=company,
            headers={
                'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """
        Create Job tests
    """

    def test_create_job(self):
        job = {"title": 'Simple', "description": 'company',
               "imageBase64": '', "state": 'Bahia', "city": 'Salvador',
               'is_remote': False, 'is_active': True, 'company_id': '4'}
        res = self.client().post(
            '/job',
            json=job,
            headers={
                'Authorization': DIRECTOR_TOKEN})

        data = json.loads(res.data)
        job_data = data['job']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(job_data['title'], job['title'])
        self.assertEqual(job_data['description'], job['description'])
        self.assertEqual(job_data['imageBase64'], job['imageBase64'])
        self.assertEqual(job_data['state'], job['state'])
        self.assertEqual(job_data['city'], job['city'])
        self.assertEqual(job_data['is_remote'], job['is_remote'])
        self.assertEqual(job_data['is_active'], job['is_active'])

    def test_create_job_error(self):
        job = {"title": 'Simple', "description": 'company',
               "imageBase64": '', "state": 'Bahia', "city": 'Salvador',
               'is_remote': False, 'is_active': True, 'company_id': '1000'}
        res = self.client().post(
            '/job',
            json=job,
            headers={
                'Authorization': DIRECTOR_TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    """
        Test for updating jobs
    """

    def test_update_job(self):
        job = {"title": 'Simple Modified', "description": 'company',
               "imageBase64": '', "state": 'Bahia', "city": 'Salvador',
               'is_remote': False, 'is_active': True, 'company_id': '1'}
        res = self.client().patch(
            '/job/2',
            json=job,
            headers={
                'Authorization': DIRECTOR_TOKEN})

        data = json.loads(res.data)
        job_data = data['job']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(job_data['title'], job['title'])
        self.assertEqual(job_data['description'], job['description'])
        self.assertEqual(job_data['imageBase64'], job['imageBase64'])
        self.assertEqual(job_data['state'], job['state'])
        self.assertEqual(job_data['city'], job['city'])
        self.assertEqual(job_data['is_remote'], job['is_remote'])
        self.assertEqual(job_data['is_active'], job['is_active'])

    def test_update_job_error(self):
        job = {"title": 'Simple Modified', "description": 'company',
               "imageBase64": '', "state": 'Bahia', "city": 'Salvador',
               'is_remote': False, 'is_active': True, 'company_id': '4'}
        res = self.client().patch(
            '/job/1000',
            json=job,
            headers={
                'Authorization': DIRECTOR_TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """
        Apply Job tests
    """

    def test_apply_job(self):
        candidate = {
            "company_id": '3',
            "job_id": '2',
            "name": 'Gabe',
            "email": 'gabirbezerra@yahoo.com.br',
            "phone": '+5571982993690'}
        res = self.client().post('/candidate/apply',
                                 json=candidate)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_apply_job_error(self):
        candidate = {
            "company_id": '1000',
            "job_id": '1000',
            "name": 'Gabe',
            "email": 'gabirbezerra@yahoo.com.br',
            "phone": '+5571982993690'}
        res = self.client().post('/candidate/apply',
                                 json=candidate)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """
        Testing get candidates with role testing
    """

    def test_get_candidates_assistant(self):
        res = self.client().get('/candidates/3', headers={
            'Authorization': ASSISTANT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_candidates_director(self):
        res = self.client().get('/candidates/3', headers={
            'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['candidates']), list)

    def test_get_candidates_error(self):
        res = self.client().get('/candidates/3?page=-2', headers={
            'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """
        Delete tests
    """

    def test_delete_job(self):
        res = self.client().delete(
            '/job/7',
            headers={
                'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_job_error(self):
        res = self.client().delete('/job/10000',
                                   headers={
                                       'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_company(self):
        res = self.client().delete('/company/14',
                                   headers={
                                       'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_company_error(self):
        res = self.client().delete('/company/10000', headers={
            'Authorization': DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
