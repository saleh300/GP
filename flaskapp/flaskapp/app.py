from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import Student, Company, db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aoun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables (run once)
with app.app_context():
    db.create_all()

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
    full_name = request.args.get('full_name')
    return render_template('student/sign_up_student.html', full_name=full_name)

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




@app.route('/submit_student_form', methods=['POST'])
def submit_student_form():
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
 
    # Redirect to a success page or back to the form
    return redirect(url_for('HomePage_student'))

@app.route('/submit_company_form', methods=['POST'])
def submit_company_form():
    # Retrieve data from the form
    Company_name = request.form.get('CoName')
    Company_email = request.form.get('CoEmail')
    Company_Pass = request.form.get('CoPass')
    Company_file = request.form.get('CoFile') # traning Schedule file

 
    # Redirect to a success page or back to the form
    return redirect(url_for('HomePage_company'))


    

if __name__ == '__main__':
    app.run(debug=True)
    