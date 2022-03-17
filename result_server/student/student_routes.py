import random

from flask import render_template, redirect, url_for, session, flash, request
from flask_mail import Message

from . import student_app
from .. import mail
from ..models import Students
from ..utils import *


def send_otp(studentdata):
    final_otp = random.randint(100000, 999999)
    msg = Message("OTP VERIFICATION", recipients=[studentdata.Email])
    msg.body = f'Your OTP for verification is {final_otp}'
    mail.send(msg)
    return final_otp


@student_app.route('/getotp', methods=['GET', 'POST'])
def get_otp():
    if request.method == 'POST':
        user_seatno = request.form.get('get_seatno')
        student_data = Students.query.filter_by(seat_no=user_seatno).first()
        if student_data:
            final_otp = send_otp(student_data)
            session['student'] = user_seatno
            session['otp'] = final_otp
            return redirect(url_for("student_app.submitotp"))
        else:
            flash("This seat no is invalid please try again")
            return render_template("getotp.html")
    return render_template("getotp.html")


@student_app.route('/submit', methods=['GET', 'POST'])
def submitotp():
    try:
        if session['otp']:
            if request.method == 'POST':
                form_otp = int(request.form.get('otp'))
                if form_otp == session['otp']:
                    session.pop('otp', None)
                    stu_id = session['student']
                    studentdata = Students.query.filter_by(seat_no=stu_id).first()
                    return render_template("view student.html", studentdata=studentdata, result=getresult(studentdata))
                else:
                    flash("Sorry Wrong OTP please input correct otp")
                    return render_template("submitotp.html")
            return render_template("submitotp.html")
    except KeyError as e:
        flash("Please Verify")
        return render_template("getotp.html")


# to send the result on email to student
@student_app.route('/emailresult', methods=['GET', 'POST'])
def emailresult():
    try:
        if session['student']:
            if request.method == 'POST':
                if request.form.get('getemail'):
                    stu_id = session['student']
                    session.pop('student', None)
                    studentdata = Students.query.filter_by(seat_no=stu_id).first()
                    make_pdf(studentdata)
                    msg = Message("RESULT 2021", recipients=[studentdata.Email])
                    msg.body = f'''This is your result of exam 2021 \n The password of the pdf is Your registered mobile number \n{getresult(studentdata)}'''
                    with open(f"{studentdata.seat_no}.pdf", 'rb') as fh:
                        msg.attach(filename=f"{studentdata.seat_no}.pdf", disposition="attachment",
                                   content_type="application/pdf",
                                   data=fh.read())
                    mail.send(msg)
                    os.remove(f"{studentdata.seat_no}.pdf")
                    flash("Your result has been send to your registered Email id")
                    return render_template("homepage.html")

                if request.form.get('Home'):
                    session.pop('student', None)
                    return render_template("homepage.html")

            flash("Please Verify")
            return render_template("getotp.html")
    except KeyError as e:
        flash("Please Verify")
        return render_template("getotp.html")
