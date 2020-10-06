import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Job, Users, Company, Candidate

def create_app(test_config=None):
    app = Flask(__name__)
    
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/jobs')
    def get_jobs():
        jobs = Job.query.all()
        jobs_response = [job.format_short() for job in jobs]
        return jsonify({
            'message': 'success',
            'status_code': 200,
            'jobs': jobs_response,
        })

    @app.route('/job', methods=['POST'])
    def create_job():
        request_value = request.get_json()

        if request_value is None:
            abort(400)

        job = Job(
            request_value['title'],
            request_value['description'],
            request_value['city'],
            request_value['state'],
            request_value['imageBase64'],
            request_value['is_active'],
            request_value['is_remote'],
            request_value['company_id']
        )
        
        job.insert()

        return jsonify({
          'status_code': 200,
          'job': job.format_long(),
          'message': 'The job was successfully created',
          'success': True,
        })
    
    @app.route('/job/<int:job_id>', methods=['PATCH'])
    def update_job(job_id):
        job = Job.query.filter_by(id=job_id).one_or_none()
        request_value = request.get_json()

        job.title = request_value['title']
        job.description = request_value['description']
        job.city = request_value['city']
        job.state = request_value['state']
        job.imageBase64 = request_value['imageBase64']
        job.is_active = request_value['is_active']
        job.is_remote = request_value['is_remote']

        job.update()

        return jsonify({
          'status_code': 200,
          'job': job.format_long(),
          'message': 'The job was successfully edited',
          'success': True,
        })

    @app.route('/job/<int:job_id>', methods=['DELETE'])
    def delete_job(job_id):
        job = Job.query.filter_by(id=job_id).one_or_none()

        if job is None: 
            abort(404)
        job.delete()

        return jsonify({
            'message': 'The Job was successfully deleted',
            'status_code': 200,
        })

    """
        Candidate's section
    """
    @app.route('/candidates')
    def get_candidates():
        candidates = Candidate.query.all()
        candidates_response = [candidate.format() for candidate in candidates]

        return jsonify({
            'message': 'success',
            'status_code': 200,
            'candidates': candidates_response,
        })

    @app.route('/candidate/apply', methods=['POST'])
    def apply_job():
        request_value = request.get_json()
        job_id = request_value['job_id']
        company_id = request_value['company_id']
    
        job = Job.query.filter_by(id=job_id).one_or_none()
        if job is None:
            abort(404)
        
        company = Company.query.filter_by(id=company_id).one_or_none()
        if company is None:
            abort(404)
        
        candidate = Candidate(
                        job_id,
                        company_id,
                        request_value['name'],
                        request_value['email'],
                        request_value['phone']
                    )

        candidate.insert()
        
        return jsonify({
            'message': 'Your application was successfully sent.',
            'status_code': 200,
        })

  
    """
    User endpoint section
    """

    #@app.route('/user')

    @app.route('/companies')
    def get_companies():
        companies = Company.query.all()
        company_response = [company.format() for company in companies]
        return jsonify({
            'message': 'success',
            'status_code': 200,
            'companies': company_response,
        })
    
    @app.route('/company', methods=['POST'])
    def create_company():
        request_value = request.get_json()

        if request_value is None:
            abort(400)

        company = Company(
            request_value['name'],
            request_value['description'],
            request_value['imageBase64'],
            request_value['state'],
            request_value['city']
        )
        company.insert()

        return jsonify({
          'status_code': 200,
          'company': company.format(),
          'message': 'The company was successfully created',
          'success': True,
        })
    
    @app.route('/company/<int:company_id>', methods=['DELETE'])
    def delete_company(company_id):
        company = Company.query.filter_by(id=company_id).one_or_none()

        if company is None: 
            abort(404)

        company.delete()

        return jsonify({
            'message': 'The Company was successfully deleted',
            'status_code': 200,
        })

    


    return app