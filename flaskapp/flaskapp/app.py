from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from datetime import datetime
from models import db, Student, Certificate, Project, Opportunity, Company, Faculty, Apply, Assigned, Experience, Trainer

app = Flask(__name__)
app.secret_key = 'aoun_for_now'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aoun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Use os.getcwd() to get the current working directory
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Initialize the database with the app
db.init_app(app)

migrate = Migrate(app, db)




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
admin.add_view(ModelView(Trainer, db.session))





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
    opportunities = Opportunity.query.all() 
    return render_template('student/HomePage_student.html', student=student, opportunities=opportunities)

@app.route('/profile')
def profile():
    student_id = session.get('student').get('StudentID')
    student = Student.query.filter_by(StudentID=student_id).first()

    if not student:
        flash('Student not found.')
        return redirect(url_for('HomePage_student'))
    
    certificates = Certificate.query.filter_by(student_id=student_id).all()
    experiences = Experience.query.filter_by(student_id=student_id).all()
    projects = Project.query.filter_by(student_id=student_id).all()

    return render_template('student/profile.html', student=student, certificates=certificates, experiences=experiences, projects=projects)


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

@app.route('/faculty/homepage')
def faculty_homepage():
    if 'faculty' not in session:
        flash('Please log in to access the faculty portal.', 'warning')
        return redirect(url_for('login'))
    return render_template('faculty/faculty_homepage.html')

@app.route('/faculty/profile')
def faculty_profile():
    if 'faculty' not in session:
        flash('Please log in to access the faculty portal.', 'warning')
        return redirect(url_for('login'))
    # Fetch faculty details from the database if needed
    return render_template('faculty/faculty_profile.html')

@app.route('/faculty/students')
def faculty_students():
    if 'faculty' not in session:
        flash('Please log in to access the faculty portal.', 'warning')
        return redirect(url_for('login'))
    # Fetch the list of students or relevant data
    return render_template('faculty/faculty_students.html')

@app.route('/faculty/documents')
def faculty_documents():
    if 'faculty' not in session:
        flash('Please log in to access the faculty portal.', 'warning')
        return redirect(url_for('login'))
    # Fetch documents or relevant data
    return render_template('faculty/faculty_documents.html')

# company section
@app.route('/sign_up_company')
def sign_up_company():
    return render_template('company/sign_up_company.html')

@app.route('/HomePage_company')
def HomePage_company():
    company = session.get('company')
    return render_template('company/HomePage_company.html', company = company)

@app.route('/comp_profile')
def comp_profile():
    company_id = session.get('company').get('CompanyID')
    company = Company.query.get(company_id)
    
    if not company:
        flash('Company not found.')
        return redirect(url_for('HomePage_company'))
    
    trainers = Trainer.query.filter_by(company_id=company_id).all()
    return render_template('company/comp_profile.html',  company=company, trainers=trainers) 

@app.route('/HomePage_trainer')
def company_trainer():
    return render_template('company/trainer.html') 

@app.route('/view_documents')
def view_documents():
    return render_template('company/view_documents.html') 



#-------------------------> start student route <--------------------------------- 

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
        StPassword=password,
        StudentID = student_id
    )
    db.session.add(new_student)
    db.session.commit()

    flash(f"Account created successfully for {first_name}",  'success')


 
    # Redirect to a success page or back to the form
    return redirect(url_for('HomePage'))




@app.route('/update_profile', methods=['POST'])
def update_profile():
    student_id = session.get('student').get('StudentID')
    student = Student.query.filter_by(StudentID=student_id).first()

    if student:
        # Update student information
        student.StFName = request.form['StFName']
        student.StLName = request.form['StLName']
        student.StPhNum = request.form['StPhNum']
        student.StCity = request.form['StCity']
        student.StEmail = request.form['StEmail']
        student.Major = request.form['Major']
        student.GPA = request.form['GPA']
        student.Interest = request.form['Interest']

        # Handle Certificates
        cer_name = request.form.get('StuCert')
        cer_details = request.form.get('CertDet')
        if cer_name:  # Ensure there is a certificate name provided
            new_certificate = Certificate(CerName=cer_name, CerDetails=cer_details, student_id=student.StudentID)
            db.session.add(new_certificate)

        # Handle Projects
        proj_name = request.form.get('ProjectName')
        proj_desc = request.form.get('ProjectDescription')
        if proj_name:  # Ensure there is a project name provided
            new_project = Project(ProjName=proj_name, ProjDesc=proj_desc, student_id=student.StudentID)
            db.session.add(new_project)

        # Handle Experiences
        exp_position = request.form.get('PositionName')
        exp_company = request.form.get('CompanyName')
        start_date_str = request.form.get('StartDate')
        end_date_str = request.form.get('EndDate')
        currently_working = 'currentlyWorking' in request.form

        if exp_position and exp_company:  # Ensure both position and company are provided
            # Convert date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str and not currently_working else None

            new_experience = Experience(
                ExpPosition=exp_position,
                ExpCompName=exp_company,
                StartDate=start_date,
                EndDate=end_date,
                CurrentlyWorking=currently_working,
                student_id=student.StudentID
            )
            db.session.add(new_experience)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
    else:
        flash('Error: Profile could not be updated.', 'danger')

    return redirect(url_for('profile'))


#-------------------------> end student route <--------------------------------- 



#-------------------------> start company route <---------------------------------

@app.route('/company_registration', methods=['POST'])
def company_registration():
    # Retrieve data from the form
    Company_name = request.form.get('CoName')
    Company_email = request.form.get('CoEmail')
    Company_Pass = request.form.get('CoPass')
    Company_file = request.files.get('CoFile')  # Use request.files to handle file uploads

    if Company_file:
        filename = secure_filename(Company_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        Company_file.save(file_path)

        # Insert into the database
        new_company = Company(
            CompName=Company_name,
            CompEmail=Company_email,
            CompPass=Company_Pass,
            CompFile=filename
        )
        db.session.add(new_company)
        db.session.commit()

        flash(f"Account created successfully for {Company_name}", 'success')
    else:
        flash("Error: File upload failed or no file provided.", 'danger')

    return redirect(url_for('HomePage'))

@app.route('/update_company_profile', methods=['POST'])
def update_company_profile():
    company_id = session.get('company').get('CompanyID')
    company = Company.query.filter_by(id=company_id).first()

    if company:
        # Update company information
        company.CompName = request.form['CompName']
        company.CompEmail = request.form['CompEmail']
        company.CompCity = request.form['CompCity']
        company.CompNum = request.form['CompNum']  # Corrected this line
        company.CompWebsite = request.form['CompWebsite']
        company.CompIndustry = request.form['CompIndustry']

        db.session.commit()
        flash('Company profile updated successfully!', 'success')
    else:
        flash('Error: Company profile could not be updated.', 'danger')

    return redirect(url_for('comp_profile'))


@app.route('/offer_coop', methods=['POST'])
def offer_coop():
    # Retrieve data from the form
    job_title = request.form.get('jobTitle')
    location = request.form.get('location')
    duration = request.form.get('duration')
    job_description = request.form.get('jobDescription')
    
    # Assuming company_id is stored in the session, retrieve it
    company_id = session.get('company').get('CompanyID')



    # Create a new Opportunity instance
    new_opportunity = Opportunity(
        OppDuration=duration,
        OppCity=location,
        OppJobTitle=job_title,
        OppJobDesc=job_description,
        company_id=company_id
    )

    # Add and commit the new opportunity to the database
    db.session.add(new_opportunity)
    db.session.commit()

    flash('Co-op opportunity offered successfully!', 'success')
    return redirect(url_for('HomePage_company'))



@app.route('/add_trainer', methods=['POST'])
def add_trainer():
    # Retrieve data from the form
    first_name = request.form.get('TraFName')
    last_name = request.form.get('TraLName')
    email = request.form.get('TraEmail')
    password = request.form.get('TraPass')
    
    # Assuming company_id is stored in the session, retrieve it
    company_id = session.get('company').get('CompanyID')

    # Insert into database
    new_trainer = Trainer(
        TraFName=first_name,
        TraLName=last_name,
        TraEmail=email,
        TraPass=password,
        company_id=company_id
    )
    
    # Add and commit the new trainer to the database
    db.session.add(new_trainer)
    db.session.commit()

    flash(f"Trainer {first_name} {last_name} added successfully!", 'success')

    # Redirect to a success page or back to the form
    return redirect(url_for('comp_profile'))



#-------------------------> end company route <--------------------------------- 

#-------------------------> start faculty route <--------------------------------- 

@app.route('/register-faculty', methods=['POST'])
def register_faculty():
    if request.method == 'POST':
        try:
            # Get form data
            FacFName = request.form['FacFName']
            FacLName = request.form['FacLName']
            FacEmail = request.form['FacEmail']
            FacID = request.form['FacID']
            FacPass = request.form['FacPass']

            # Create a new Faculty object
            new_faculty = Faculty(FacID=FacID, FacFName=FacFName, FacLName=FacLName, FacEmail=FacEmail, FacPass=FacPass)

            print(new_faculty)  # For debugging

            # Add to the database
            db.session.add(new_faculty)
            db.session.commit()

            flash('Faculty account created successfully!', 'success')
            return redirect(url_for('HomePage'))
        
        except Exception as e:
            db.session.rollback()
            print(f'Error: {str(e)}')  # For debugging
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('HomePage'))


#-------------------------> strat Login - logout route <--------------------------------- 

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if role == 'student':
        user = Student.query.filter_by(StEmail=email).first()
        if user and user.StPassword == password:
            # Store necessary user information in the session
            session['student'] = {
                'StudentID': user.StudentID,
                'StFName': user.StFName,
                'StLName': user.StLName,
                'StEmail': user.StEmail
            }
            return redirect(url_for('HomePage_student'))
        else:
            flash('Invalid credentials for student, please try again.')
            return redirect(url_for('HomePage'))

    elif role == 'company':
        user = Company.query.filter_by(CompEmail=email).first()
        if user and user.CompPass == password:
            if user.verify:
                # Store necessary user information in the session (if needed)
                session['company'] = {
                    'CompanyID': user.id,
                    'CompName': user.CompName,
                    'CompEmail': user.CompEmail
                }
                return redirect(url_for('HomePage_company'))
            else:
                flash('Your account is under review. Please wait for verification.', 'warning')
                return redirect(url_for('HomePage'))
        else:
            flash('Invalid credentials for company, please try again.')
            return redirect(url_for('HomePage'))
    
    elif role == 'Trainer':  # Handle Trainer login
        user = Trainer.query.filter_by(TraEmail=email).first()
        if user and user.TraPass == password:
            session['trainer'] = {
                'TrainerID': user.TrainerID,
                'TraFName': user.TraFName,
                'TraLName': user.TraLName,
                'TraEmail': user.TraEmail
            }
            return redirect(url_for('company_trainer'))  # You'll need to create this route and template
        else:
            flash('Invalid credentials for trainer, please try again.')
            return redirect(url_for('HomePage'))

    elif role == 'faculty':  # Handle Faculty login
        user = Faculty.query.filter_by(FacEmail=email).first()
        if user and user.FacPass == password:
            session['faculty'] = {
                'FacID': user.FacID,
                'FacFName': user.FacFName,
                'FacLName': user.FacLName,
                'FacEmail': user.FacEmail
            }
            return redirect(url_for('faculty_homepage'))  # You'll need to create this route and template
        else:
            flash('Invalid credentials for faculty, please try again.')
            return redirect(url_for('HomePage'))

    else:
        flash('Invalid role selected.')
        return redirect(url_for('HomePage'))



@app.route('/logout')
def logout():
    # Remove student and company data from the session
    session.pop('student', None)
    session.pop('company', None)
    session.pop('trainer', None)
    session.pop('faculty', None)
    
    flash('You have been logged out.', 'info')
    return redirect(url_for('HomePage'))

#-------------------------> end Login - logout route <--------------------------------- 

if __name__ == '__main__':
    app.run(debug=True)
