# db.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
# database 

class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True)
    StFName = db.Column(db.String(100), nullable=False)
    StLName = db.Column(db.String(100), nullable=False)
    StEmail = db.Column(db.String(100), unique=True, nullable=False)
    StPhNum = db.Column(db.String(15), nullable=True)
    StCity = db.Column(db.String(50), nullable=True)
    GPA = db.Column(db.Float, nullable=True)
    StPic = db.Column(db.String(200), nullable=True, default='default.jpg')
    Major = db.Column(db.String(50), nullable=True)
    Interest = db.Column(db.String(100), nullable=True)
    StPassword = db.Column(db.String(100), nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.FacID'), nullable=True)
    faculty = db.relationship('Faculty', backref='students')

    certificates = db.relationship('Certificate', backref='student', lazy=True)
    projects = db.relationship('Project', backref='student', lazy=True)
    experiences = db.relationship('Experience', backref='student_experiences', lazy=True)
    applications = db.relationship('Apply', backref='applied_student', lazy=True)  # Match the renamed backref



class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CerName = db.Column(db.String(100), nullable=False)
    CerDetails = db.Column(db.Text, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ProjName = db.Column(db.String(100), nullable=False)
    ProjDesc = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ExpPosition = db.Column(db.String(100), nullable=False)
    ExpCompName = db.Column(db.String(100), nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    EndDate = db.Column(db.DateTime, nullable=True)
    CurrentlyWorking = db.Column(db.Boolean, nullable=False, default=False)

    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)
    student = db.relationship('Student', backref='student_experiences')  # Renamed backref

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    OppDuration = db.Column(db.String(50), nullable=False)
    OppCity = db.Column(db.String(50), nullable=False)
    OppJobTitle = db.Column(db.String(100), nullable=False)
    OppJobDesc = db.Column(db.Text, nullable=False)
    open_date = db.Column(db.DateTime, nullable=False)
    close_date = db.Column(db.DateTime, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    applications = db.relationship('Apply', backref='applied_opportunities', lazy=True)




class Trainer(db.Model):
    TrainerID = db.Column(db.Integer, primary_key=True)
    TraFName = db.Column(db.String(100), nullable=False)
    TraLName = db.Column(db.String(100), nullable=False)
    TraEmail = db.Column(db.String(100), unique=True, nullable=False)
    TraPass = db.Column(db.String(100), nullable=False)
    
    # Relationship with the Company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    assigned_company = db.relationship('Company', backref='trainers', lazy=True)
    
    # Relationship with Assigned (Student Assignments)
    trainer_assignments = db.relationship('Assigned', backref='assigned_trainer', lazy=True)

    
    def __repr__(self):
        return (f'<Trainer ID: {self.TrainerID}, '
                f'First Name: {self.TraFName}, '
                f'Last Name: {self.TraLName}, '
                f'Email: {self.TraEmail}, '
                f'Company ID: {self.company_id}>')


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CompName = db.Column(db.String(100), nullable=False)
    CompCity = db.Column(db.String(50), nullable=True)
    CompNum = db.Column(db.String(15), nullable=True)
    CompEmail = db.Column(db.String(100), nullable=False)
    CompWebsite = db.Column(db.String(100), nullable=True)
    CompIndustry = db.Column(db.String(100), nullable=True)
    CompPic = db.Column(db.String(200), nullable=True)
    CompPass = db.Column(db.String(100), nullable=False)
    CompFile = db.Column(db.String(100), nullable=False)
    verify = db.Column(db.Boolean, nullable=True, default=False)
    CompLogo = db.Column(db.String(100), nullable=True)

    opportunities = db.relationship('Opportunity', backref='company', lazy=True)
    # trainers backref is already defined in the Trainer model




class Faculty(db.Model):
    FacID = db.Column(db.Integer, primary_key=True)
    FacFName = db.Column(db.String(100), nullable=False)
    FacLName = db.Column(db.String(100), nullable=False)
    FacEmail = db.Column(db.String(100), nullable=False)
    FacPass = db.Column(db.String(100), nullable=False)

    assignments = db.relationship('Assigned', backref='faculty_assignments', lazy=True)  # Renamed backref




class Apply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)
    applied_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')

    student = db.relationship('Student', backref='applications_apply')  # Renamed backref
    opportunity = db.relationship('Opportunity', backref='applied_opportunities')


class Assigned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.FacID'), nullable=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.TrainerID'), nullable=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)

    # Relationships
    student = db.relationship('Student', backref='student_assignments', lazy=True)
    faculty = db.relationship('Faculty', backref='faculty_assigned', lazy=True)
    trainer = db.relationship('Trainer', lazy=True)
    opportunity = db.relationship('Opportunity', backref='opportunity_assigned', lazy=True)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(100), nullable=False)
    doc_path = db.Column(db.String(200), nullable=False)  # Path to the uploaded file
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    approved_by_trainer = db.Column(db.Boolean, nullable=False, default=False)
    approved_date = db.Column(db.DateTime, nullable=True)
    trainer_comment = db.Column(db.String(255), nullable=True)  # New field for comments
    status = db.Column(db.String(50), default='Pending')
    week_number = db.Column(db.Integer)  
    
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.TrainerID'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.FacID'), nullable=True)
    
    # Relationships
    student = db.relationship('Student', backref='documents', lazy=True)
    trainer = db.relationship('Trainer', backref='trainer_documents', lazy=True)
    faculty = db.relationship('Faculty', backref='faculty_documents', lazy=True)

    def __repr__(self):
        return (f'<Document ID: {self.id}, '
                f'Document Name: {self.doc_name}, '
                f'Uploaded By: {self.student_id}, '
                f'Approved By Trainer: {self.approved_by_trainer}>')
