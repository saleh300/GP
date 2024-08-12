from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# homePage section
@app.route("/")
def HomePage():
    return render_template("HomePage.html")



# student section
@app.route('/sign_in_student')
def sign_in_student():
    return render_template('student/sign_in_student.html')

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
@app.route('/sign_in_faculty')
def sign_in_faculty():
    return render_template('faculty/sign_in_faculty.html') 

@app.route('/sign_up_faculty')
def sign_up_faculty():
    return render_template('faculty/sign_up_faculty.html')



# company section
@app.route('/sign_in_company')
def sign_in_company():
    return render_template('company/sign_in_company.html') 

@app.route('/sign_up_company')
def sign_up_company():
    return render_template('company/sign_up_company.html')

@app.route('/HomePage_company')
def HomePage_company():
    return render_template('company/HomePage_company.html')

@app.route('/offer_COOP')
def offer_COOP():
    return render_template('company/offer_COOP.html') 

@app.route('/comp_profile')
def comp_profile():
    return render_template('company/comp_profile.html') 

@app.route('/view_documents')
def view_documents():
    return render_template('company/view_documents.html') 


if __name__ == "__main__":
    app.run(debug=True)