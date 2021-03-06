import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

database_name = os.environ.get('DATABASE_NAME')
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Company(db.Model):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    imageBase64 = Column(String)
    state = Column(String)
    city = Column(String)
    job = db.relationship('Job', backref='company', lazy=True)
    candidates = db.relationship('Candidate', backref='company', lazy=True)

    def __init__(self, name, description, imageBase64, state, city):
        self.name = name
        self.description = description
        self.imageBase64 = imageBase64
        self.state = state
        self.city = city

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'imageBase64': self.imageBase64,
            'state': self.state,
            'city': self.city
        }


class Job(db.Model):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    city = Column(String)
    state = Column(String)
    imageBase64 = Column(String)
    is_active = Column(Boolean)
    is_remote = Column(Boolean)
    candidates = db.relationship('Candidate', backref='job', lazy=True)
    company_id = Column(Integer, db.ForeignKey('company.id'), nullable=False)

    def __init__(self, title, description, city, state, imageBase64,
                 is_active, is_remote, company_id):
        self.title = title
        self.description = description
        self.city = city
        self.state = state
        self.imageBase64 = imageBase64
        self.is_active = is_active
        self.is_remote = is_remote
        self.company_id = company_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_short(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'city': self.city,
            'state': self.state,
            'imageBase64': self.imageBase64,
            'is_active': self.is_active,
            'is_remote': self.is_remote,
        }

    def format_long(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'city': self.city,
            'state': self.state,
            'imageBase64': self.imageBase64,
            'is_active': self.is_active,
            'is_remote': self.is_remote,
        }


class Candidate(db.Model):
    __tablename__ = 'candidate'

    id = Column(Integer, primary_key=True)
    job_id = Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    company_id = Column(db.Integer, db.ForeignKey(
        'company.id'), nullable=False)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    def __init__(self, job_id, company_id, name, email, phone):
        self.job_id = job_id
        self.company_id = company_id
        self.name = name
        self.email = email
        self.phone = phone

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'job_id': self.job_id,
            'company_id': self.company_id,
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
