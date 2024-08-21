from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aoun.db'


db = SQLAlchemy(app)

# homePage section
@app.route("/")
@app.route("/home")
def HomePage():
    return render_template("HomePage.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")



# student section


@app.route('/sign_up_student')
def sign_up_student():
    return render_template('student/sign_up_student.html')

@app.route('/HomePage_student')
def HomePage_student():
    return render_template('student/HomePage_student.html')

@app.route('/profile')
def profile():
    return render_template('student/profile.html')

@app.route('/appliaction')
def appliaction():
    return render_template('student/appliaction.html')

@app.route('/doucment')
def doucment():
    return render_template('student/doucment.html')



# faculty section


@app.route('/sign_up_faculty')
def sign_up_faculty():
    return render_template('faculty/sign_up_faculty.html')



# company section


@app.route('/sign_up_company')
def sign_up_company():
    return render_template('company/sign_up_company.html')

@app.route('/HomePage_company')
def HomePage_company():
    return render_template('company/HomePage_company.html')

@app.route('/comp_profile')
def comp_profile():
    return render_template('company/comp_profile.html') 

@app.route('/view_documents')
def view_documents():
    return render_template('company/view_documents.html') 






# database 

class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True)
    StFName = db.Column(db.String(100), nullable=False)
    StLName = db.Column(db.String(100), nullable=False)
    StEmail = db.Column(db.String(100), unique=True, nullable=False)
    StPhNum = db.Column(db.String(15), nullable=False)
    StCity = db.Column(db.String(50), nullable=False)
    GPA = db.Column(db.Float, nullable=False)
    StPic = db.Column(db.String(200), nullable=True, default='default.jpg')
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




if __name__ == "__main__":
    app.run(debug=True)