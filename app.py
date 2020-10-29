import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Candidate, Company, Job, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)

    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    ITEMS_PER_PAGE = 10

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    Company's section
    """

    """
        Get all companies registered
    """
    @app.route('/companies')
    def get_companies():
        companies = Company.query.all()
        company_response = [company.format() for company in companies]
        page = request.args.get('page', 1, type=int)

        if page < 0:
            abort(422)

        start = (page - 1) * ITEMS_PER_PAGE
        end = page * ITEMS_PER_PAGE

        return jsonify({
            'success': True,
            'status_code': 200,
            'companies': company_response[start:end],
        })

    """
        Allows logged users to create companies
    """
    @app.route('/company', methods=['POST'])
    @requires_auth('create:companies')
    def create_company(jwt):
        request_value = request.get_json()
        if request_value is None:
            abort(400)

        properties = ['name', 'description', 'imageBase64', 'state', 'city']
        for prop in properties:
            if prop not in request_value:
                abort(400)

        if request_value['name'] is None:
            abort(400)

        if request_value['state'] is None or request_value['city'] is None:
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

    """
        Allows logged users to update existing companies
    """
    @app.route('/company/<int:company_id>', methods=['PATCH'])
    @requires_auth('update:companies')
    def update_company(jwt, company_id):
        company = Company.query.filter_by(id=company_id).one_or_none()
        request_value = request.get_json()

        if company is None:
            abort(404)

        if 'name' in request_value:
            company.name = request_value['name']

        if 'description' in request_value:
            company.name = request_value['description']

        if 'imageBase64' in request_value:
            company.imageBase64 = request_value['imageBase64']

        if 'state' in request_value:
            company.state = request_value['state']

        if 'city' in request_value:
            company.city = request_value['city']

        company.update()

        return jsonify({
            'status_code': 200,
            'company': company.format(),
            'message': 'The Company was successfully edited',
            'success': True,
        })

    """
        Allows logged users to delete existing companies
    """
    @app.route('/company/<int:company_id>', methods=['DELETE'])
    @requires_auth('delete:companies')
    def delete_company(jwt, company_id):
        company = Company.query.filter_by(id=company_id).one_or_none()

        if company is None:
            abort(404)

        candidates = Candidate.query.filter_by(company_id=company_id).all()
        for candidate in candidates:
            candidate.delete()

        jobs = Job.query.filter_by(company_id=company_id).all()
        for job in jobs:
            job.delete()

        company.delete()

        return jsonify({
            'success': True,
            'message': 'The Company was successfully deleted',
            'status_code': 200,
        })

    """
        Job's section
    """

    """
        Gets all registered jobs
    """
    @app.route('/jobs')
    def get_jobs():
        jobs = Job.query.all()
        jobs_response = [job.format_short() for job in jobs]
        page = request.args.get('page', 1, type=int)

        if page < 0:
            abort(422)

        start = (page - 1) * ITEMS_PER_PAGE
        end = page * ITEMS_PER_PAGE

        return jsonify({
            'message': 'success',
            'success': True,
            'status_code': 200,
            'jobs': jobs_response[start:end],
        })

    """
        Allows logged users to create jobs for existing companies
    """
    @app.route('/job', methods=['POST'])
    @requires_auth('create:jobs')
    def create_job(jwt):
        request_value = request.get_json()

        if request_value is None:
            abort(400)

        company_id = request_value['company_id']
        company = Company.query.filter_by(id=company_id).one_or_none()

        if company is None:
            abort(400)

        job = Job(
            request_value['title'],
            request_value['description'],
            request_value['city'],
            request_value['state'],
            request_value['imageBase64'],
            request_value['is_active'],
            request_value['is_remote'],
            company_id
        )

        job.insert()

        return jsonify({
            'status_code': 200,
            'job': job.format_long(),
            'message': 'The job was successfully created',
            'success': True,
        })

    """
        Allows logged users to update existing jobs
    """
    @app.route('/job/<int:job_id>', methods=['PATCH'])
    @requires_auth('update:jobs')
    def update_job(jwt, job_id):
        job = Job.query.filter_by(id=job_id).one_or_none()

        if job is None:
            abort(404)

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

    """
        Allows logged users to delete existing jobs
    """
    @app.route('/job/<int:job_id>', methods=['DELETE'])
    @requires_auth('delete:jobs')
    def delete_job(jwt, job_id):
        job = Job.query.filter_by(id=job_id).one_or_none()
        candidates = Candidate.query.filter_by(job_id=job_id).all()
        for candidate in candidates:
            candidate.delete()

        if job is None:
            abort(404)

        job.delete()

        return jsonify({
            'success': True,
            'message': 'The Job was successfully deleted',
            'status_code': 200,
        })

    """
        Candidate's section
    """

    """
        Allows directors users to see candidates
    """
    @app.route('/candidates/<int:job_id>')
    @requires_auth('get:job_candidates')
    def get_candidates_by_job(jwt, job_id):
        candidates = Candidate.query.filter_by(job_id=job_id).all()
        candidates_response = [candidate.format() for candidate in candidates]

        page = request.args.get('page', 1, type=int)

        if page < 0:
            abort(422)

        start = (page - 1) * ITEMS_PER_PAGE

        end = page * ITEMS_PER_PAGE
        return jsonify({
            'message': 'success',
            'success': True,
            'status_code': 200,
            'candidates': candidates_response[start:end],
        })

    """
        Adds a candidate to an specific job application
    """
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
            'success': True
        })

    """
        Error handlers
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Sorry, we couldn't handle your request."
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
