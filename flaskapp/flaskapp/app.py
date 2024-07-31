from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("HomePage.html")




@app.route('/sign_in_student')
def sign_in_student():
    return render_template('sign_in_student.html')

@app.route('/sign_up_student')
def sign_up_student():
    return render_template('sign_up_student.html')

@app.route('/HomePage_student')
def HomePage_student():
    return render_template('HomePage_student.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/sign_in_faculty')
def sign_in_faculty():
    return render_template('sign_in_faculty.html') 

@app.route('/sign_up_faculty')
def sign_up_faculty():
    return render_template('sign_up_faculty.html')

@app.route('/sign_in_company')
def sign_in_company():
    return render_template('sign_in_company.html') 

@app.route('/sign_up_company')
def sign_up_company():
    return render_template('sign_up_company.html')




if __name__ == "__main__":
    app.run(debug=True)