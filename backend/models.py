import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_name = 'full_project'
database_path = "postgres://postgres:21092000@{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    migrate = Migrate(app, db)




class Job(db.Model):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    city = Column(String)
    state = Column(String)
    imageBase64 = Column(String)
    is_active = Column(Boolean)
    candidates = Column(db.ARRAY(db.String))
    is_remote = Column(Boolean)
    company_id = Column(Integer, db.ForeignKey('company.id'), nullable=False)

    def __init__(self, title, description, city, state, imageBase64, is_active, candidates, is_remote, company_id):
        self.title = title
        self.description = description
        self.city = city
        self.state = state
        self.imageBase64 = imageBase64
        self.is_active = is_active
        self.candidates = candidates
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
            'candidates': self.candidates,
            'imageBase64': self.imageBase64,
            'is_active': self.is_active,
            'is_remote': self.is_remote,
        }


class Company(db.Model):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    imageBase64 = Column(String)
    state=Column(String)
    city=(String)
    job = db.relationship('Job', backref='company', lazy=True)

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


class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role

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
            'email': self.email,
            'role': self.role
        }


