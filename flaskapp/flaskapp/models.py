from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLAlCHEMY_DATABASE_URL'] = 'sqlite:///aoun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True)
    StFName = db.Column(db.String(100), nullable=False)
    StLName = db.Column(db.String(100), nullable=False)
    StEmail = db.Column(db.String(100), unique=True, nullable=False)
    StPhNum = db.Column(db.String(15), nullable=False)
    StCity = db.Column(db.String(50), nullable=False)
    GPA = db.Column(db.Float, nullable=False)
    StPic = db.Column(db.String(200), nullable=True)
    Major = db.Column(db.String(50), nullable=False)
    Interest = db.Column(db.String(100), nullable=True)
    StPassword = db.Column(db.String(100), nullable=False)

    certificates = db.relationship('Certificate', backref='student', lazy=True)
    projects = db.relationship('Project', backref='student', lazy=True)
    applications = db.relationship('Apply', backref='student', lazy=True)


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CerName = db.Column(db.String(100), nullable=False)
    CerDetails = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ProjName = db.Column(db.String(100), nullable=False)
    ProjDesc = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)


class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    OppDuration = db.Column(db.Integer, nullable=False)
    OppCity = db.Column(db.String(50), nullable=False)
    OppJobTitle = db.Column(db.String(100), nullable=False)
    OppJobDesc = db.Column(db.Text, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    applications = db.relationship('Apply', backref='opportunity', lazy=True)
    assignments = db.relationship('Assigned', backref='opportunity', lazy=True)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CompName = db.Column(db.String(100), nullable=False)
    CompCity = db.Column(db.String(50), nullable=False)
    CompNum = db.Column(db.String(15), nullable=False)
    CompEmail = db.Column(db.String(100), nullable=False)
    CompWebsite = db.Column(db.String(100), nullable=True)
    CompIndustry = db.Column(db.String(100), nullable=False)
    CompPic = db.Column(db.String(200), nullable=True)
    CompPass = db.Column(db.String(100), nullable=False)

    opportunities = db.relationship('Opportunity', backref='company', lazy=True)


class Faculty(db.Model):
    FacID = db.Column(db.Integer, primary_key=True)
    FacFName = db.Column(db.String(100), nullable=False)
    FacLName = db.Column(db.String(100), nullable=False)
    FacEmail = db.Column(db.String(100), nullable=False)
    FacPass = db.Column(db.String(100), nullable=False)

    assignments = db.relationship('Assigned', backref='faculty', lazy=True)


class Apply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)


class Assigned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.FacID'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)
