import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Candidate, Job, Company, setup_db

TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
TEST_DATABASE_NAME = os.environ.get('TEST_DATABASE_NAME')

DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5YOThWeDhaUHZtSjJBbV9hWVRFWCJ9.eyJpc3MiOiJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQxMTg0MjUwNTU0MDgzMzg5MjEiLCJhdWQiOlsiZnVsbFByb2plY3QiLCJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA0MDA3MTIzLCJleHAiOjE2MDQwOTM1MjMsImF6cCI6IjhBZDhuWDMybWJxMk9XWHRqa0luYWxVOVFCa203TGI4Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpjb21wYW5pZXMiLCJjcmVhdGU6am9icyIsImRlbGV0ZTpjb21wYW5pZXMiLCJkZWxldGU6am9icyIsImdldDpjYW5kaWRhdGVzIiwiZ2V0OmpvYl9jYW5kaWRhdGVzIiwidXBkYXRlOmNvbXBhbmllcyIsInVwZGF0ZTpqb2JzIl19.cjPD2c_5j0140UOJIE1feVxPC21Xu7j-xw94u5-42X0McWBY7cLgVgkFzOXLkng3jdaW98hiLCxE5mpC2BuyBF5O98KH-IhD3cf5oweOCWpZohXuixZ7kjGtyv7-kVCj1M-CSOGRR2617o27tG3YDoEMllfDZ6S6uIfq7JNdK9zWiegxfMe-2v1f9yzdDhEEUgZRyX_-Re2kh5IyzkEnhSHwfRhC1B5CVx3xQxohauFQDS1T4bQ1PoUG-PywUeALdRLl0LZeFKAmLJSSp9GFX_WlNcv4fGgADakG3yJzj_aRL63de212zVGlfCbAP0maQZocjcz7v_c1qt8mncd96w'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5YOThWeDhaUHZtSjJBbV9hWVRFWCJ9.eyJpc3MiOiJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDI3NDg5ODcxMzE5Mjc4NzM3NzgiLCJhdWQiOlsiZnVsbFByb2plY3QiLCJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA0MDA3MDEzLCJleHAiOjE2MDQwOTM0MTMsImF6cCI6IjhBZDhuWDMybWJxMk9XWHRqa0luYWxVOVFCa203TGI4Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpjb21wYW5pZXMiLCJjcmVhdGU6am9icyIsImRlbGV0ZTpjb21wYW5pZXMiLCJkZWxldGU6am9icyIsInVwZGF0ZTpjb21wYW5pZXMiLCJ1cGRhdGU6am9icyJdfQ.x-fuVLvZ-vGwDBWv4UrHmx0yBi_0xN6VvzIz_y5_1yEODas8JAqEt0WwOirTzZkF5z0YcYxe83WoV0H3jJ0X5LTKtrE0_w2N6YX8xt-AAT6oI3FtjiZWUKNXlqNsGg_cqDuXye1Wxo2Z6pqrUvNgACZMHDPh03DnA_J4koAA_B9kpC2a3VJdGu5cruzscpk1dlgRlDKocEQzIJp6aDIg1Gyoq20F9wcB9jOkJ_NsAZ7WiM9eL5sNLtREnRprvC6rTJuhWGIC1XylZm6pNgm-dMrahcgm4mIYYyGB8WGTfLMVzUmknkfDsSWdRGWGUX7Q12_6QWeD3pll0AMsO1OySw'
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
                'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)})

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
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

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
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

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
            '/company/1',
            json=company,
            headers={
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})
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
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})
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
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

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
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

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
            '/job/1',
            json=job,
            headers={
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

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
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """
        Apply Job tests
    """

    def test_apply_job(self):
        candidate = {
            "company_id": '1',
            "job_id": '1',
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
            "company_id": '7',
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
        res = self.client().get('/candidates/1', headers={
            'Authorization': 'Bearer {}'.format(ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_candidates_director(self):
        res = self.client().get('/candidates/1', headers={
            'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(type(data['candidates']), list)

    def test_get_candidates_error(self):
        res = self.client().get('/candidates/1?page=-2', headers={
            'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """
        Delete tests
    """

    def test_delete_job(self):
        res = self.client().delete(
            '/job/1',
            headers={
                'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_job_error(self):
        res = self.client().delete('/job/10000',
                                   headers={
                                       'Authorization': 'Bearer {}'
                                       .format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_company(self):
        res = self.client().delete('/company/1',
                                   headers={
                                       'Authorization': 'Bearer {}'
                                       .format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_company_error(self):
        res = self.client().delete('/company/10000', headers={
            'Authorization': 'Bearer {}'
            .format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
