from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from models import db, Student, Certificate, Project, Opportunity, Company, Faculty, Apply, Assigned, Experience

app = Flask(__name__)
app.secret_key = 'aoun_for_now'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aoun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables (run once)
with app.app_context():
    db.create_all()

# Initialize Flask-Admin
admin = Admin(app, name='Aoun Admin', template_mode='bootstrap3')

# Add views for your models
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Certificate, db.session))
admin.add_view(ModelView(Experience, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Opportunity, db.session))
admin.add_view(ModelView(Company, db.session))
admin.add_view(ModelView(Faculty, db.session))
admin.add_view(ModelView(Apply, db.session))
admin.add_view(ModelView(Assigned, db.session))


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
    student = session.get('student')
    return render_template('student/HomePage_student.html', student=student)

@app.route('/profile')
def profile():
    student_id = session.get('student').get('StudentID')
    student = Student.query.filter_by(StudentID=student_id).first()
    return render_template('student/profile.html', student=student)

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

@app.route('/student_registration', methods=['POST'])
def student_registration():
    # Retrieve data from the form
    first_name = request.form.get('StuFName')
    last_name = request.form.get('StuLName')
    email = request.form.get('StuEamil')
    student_id = request.form.get('StuId')
    password = request.form.get('StuPass')

    # Insert into database
    new_student = Student(
        StFName=first_name,
        StLName=last_name,
        StEmail=email,
        StPassword=password
    )
    db.session.add(new_student)
    db.session.commit()

    flash(f"Account created successfully for {first_name}")

    # Query the students
    students = Student.query.all()
    for student in students:
        print(student)
 
    # Redirect to a success page or back to the form
    return redirect(url_for('HomePage'))


@app.route('/update_profile', methods=['POST'])
def update_profile():
    student_id = session.get('student').get('StudentID')
    student = Student.query.filter_by(StudentID=student_id).first()

    if student:
        student.StFName = request.form['StFName']
        student.StLName = request.form['StLName']
        student.StPhNum = request.form['StPhNum']
        student.StCity = request.form['StCity']
        student.StEmail = request.form['StEmail']
        student.Major = request.form['Major']
        student.GPA = request.form['GPA']
        student.Interest = request.form['Interest']

        db.session.commit()
        flash('Profile updated successfully!')
    else:
        flash('Error: Profile could not be updated.')

    return redirect(url_for('profile'))

@app.route('/company_registration', methods=['POST'])
def company_registration():
    # Retrieve data from the form
    Company_name = request.form.get('CoName')
    Company_email = request.form.get('CoEmail')
    Company_Pass = request.form.get('CoPass')
    Company_file = request.form.get('CoFile') # training Schedule file

    # Insert into database (logic not shown in your original code)
    # Insert into database
    new_student = Student(
        CompName=Company_name,
        CompEmail=Company_email,
        CompPass=Company_Pass,
        StPassword=Company_file
    )


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if role == 'student':
        user = Student.query.filter_by(StEmail=email).first()
        if user and user.StPassword == password:
            session['student'] = {'StudentID': user.StudentID}  # Store only StudentID
            return redirect(url_for('HomePage_student'))
        else:
            flash('Invalid credentials for student, please try again.')
            return redirect(url_for('HomePage'))



    elif role == 'company':
        user = Company.query.filter_by(CompEmail=email).first()
        if user and user.CompPass == password:
            return redirect(url_for('HomePage_company'))
        else:
            flash('Invalid credentials for company, please try again.')
            return redirect(url_for('HomePage'))

    else:
        flash('Invalid role selected.')
        return redirect(url_for('HomePage'))


if __name__ == '__main__':
    app.run(debug=True)
