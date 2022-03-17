

from flask import render_template, redirect, url_for, session,flash,request

from . import app


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        if request.form.get('facultysignup'):
            return redirect(url_for('faculty_app.add_faculty'))
        elif request.form.get('getresult'):
            return redirect(url_for('student_app.get_otp'))
        elif request.form.get('facultylogin'):
            return redirect(url_for('faculty_app.login'))
    return render_template('homepage.html')
