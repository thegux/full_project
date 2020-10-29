import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Candidate, Job, Company, setup_db

TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
TEST_DATABASE_NAME = os.environ.get('TEST_DATABASE_NAME')

DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5YOThWeDhaUHZtSjJBbV9hWVRFWCJ9.eyJpc3MiOiJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQxMTg0MjUwNTU0MDgzMzg5MjEiLCJhdWQiOlsiZnVsbFByb2plY3QiLCJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAzOTcwNTgyLCJleHAiOjE2MDM5Nzc3ODIsImF6cCI6IjhBZDhuWDMybWJxMk9XWHRqa0luYWxVOVFCa203TGI4Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpjb21wYW5pZXMiLCJjcmVhdGU6am9icyIsImRlbGV0ZTpjb21wYW5pZXMiLCJkZWxldGU6am9icyIsImdldDpjYW5kaWRhdGVzIiwiZ2V0OmpvYl9jYW5kaWRhdGVzIiwidXBkYXRlOmNvbXBhbmllcyIsInVwZGF0ZTpqb2JzIl19.EMskpNk178o-RiiegWASxZ9bFb_bSbxY7GHgl5HG0Vp7ABWLDkrakDMgdhE-Lzo0g1l69_9GB_dbDJU93gqmrP_3i8CrUOFLgLhUKTWaCwEsRQx3BHkE0el-Vg4byDnh5qdBLJYuoJTpPOchVK76mwLLB2RFC2k2ySSCgV4QSoMqoCaZlO5AiNkPLA_TS-a0h81wPItyPTAwQ10u8mLOg43MzekRrMDOhLnHrdUchx81dyWLAEN_OVemDn2ynmIzY_c7vNV6b9WNjIpJgdRkQZNNl5gC08oVCUA2cs7oNHxYDx5iP-PZL2JBGoqCJOy3_7AlZnTQz6m-t7J8XH_Qcw'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5YOThWeDhaUHZtSjJBbV9hWVRFWCJ9.eyJpc3MiOiJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDI3NDg5ODcxMzE5Mjc4NzM3NzgiLCJhdWQiOlsiZnVsbFByb2plY3QiLCJodHRwczovL3RoZWd1eC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAzOTcwMjY5LCJleHAiOjE2MDM5Nzc0NjksImF6cCI6IjhBZDhuWDMybWJxMk9XWHRqa0luYWxVOVFCa203TGI4Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpjb21wYW5pZXMiLCJjcmVhdGU6am9icyIsImRlbGV0ZTpjb21wYW5pZXMiLCJkZWxldGU6am9icyIsInVwZGF0ZTpjb21wYW5pZXMiLCJ1cGRhdGU6am9icyJdfQ.ZUA33Tuu-CJ_t19YBpbVw98W6LKjojxdmXzZ5epVAv69hmocLUXofFX-0vf7wbDtrSi2LNZc7xO8OD6p3ajKhPfELI7Iu53uBzbNyzRJhaA0FzBqkOAOcII0qsMb45PpLN5azS1QPaQvUWMn6HXsepU5QkVcdiH-SRBWbl1lhLkF-fWuObCXI3mh9XINbk8ZL09nzslczTKbLgjQB4DShGKNgJ5aqMUHY044QQDBsGCnmI4ZKg5OAHCsGTUz8sAT_OswjwMcevLctxs4fQ69EwxvMUZAjzASrCxs4NiQwGv303x2yQV27tJKkzP4w4LNgByOryc9SeDJBTChPGjJHA'
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
        res = self.client().post('/company',
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
        res = self.client().post('/company',
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
        res = self.client().post('/company',
                                 json=company,
                                 headers={
                                     'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_company(self):
        company = {"description": 'company',
                   "imageBase64": '', "state": 'Bahia', "city": 'Lauro de Freitas'}
        res = self.client().patch('/company/2', 
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
        company = {"description": 'company',
                   "imageBase64": '', "state": 'Bahia', "city": 'Lauro de Freitas'}
        res = self.client().patch('/company/10000', 
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
        res = self.client().post('/job',
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
        res = self.client().post('/job',
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
                   'is_remote': False, 'is_active': True, 'company_id': '4'}
        res = self.client().patch('/job/2',
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
        res = self.client().patch('/job/1000',
                                 json=job,
                                 headers={
                                     'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    """
        Delete tests
    """
    def test_delete_company_error(self):
        res = self.client().delete('/company/3', 
                                  headers={
                                     'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_company_error(self):
        res = self.client().delete('/company/10000', 
                                  headers={
                                     'Authorization': 'Bearer {}'.format(DIRECTOR_TOKEN)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()
