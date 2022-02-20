import random
from result_server import app, db, mail
from result_server.backendfiles import *
from flask import render_template, redirect, url_for, session,flash,request
from flask_mail import Mail, Message
from sqlalchemy import exc
from flask_login import login_user, current_user, logout_user, login_required


from result_server.models import Students, Faculty

def send_otp(studentdata):
    final_otp = random.randint(100000, 999999)
    print(final_otp)
    msg = Message("OTP VERIFICATION", recipients=[studentdata.Email])
    msg.body = f'Your OTP for verification is {final_otp}'
    mail.send(msg)
    return final_otp

"""paginate this route"""
# To show ALL THE STUNDENTS DATA TO THE Faculty after login
@app.route('/show', methods=['GET', 'POST'])
@login_required
def showall():
    page = request.args.get('page', 1, type=int)
    allstudents = Students.query.paginate(
        page, 10, False)
    if request.method == 'POST':
        if request.form.get('Add student'):
            return redirect(url_for("addstudent"))
        elif request.form.get('Logout'):
            return redirect(url_for('logout'))
    next_url = url_for('showall', page=allstudents.next_num) \
        if allstudents.has_next else None
    prev_url = url_for('showall', page=allstudents.prev_num) \
        if allstudents.has_prev else None
    return render_template("allstudents.html", allstudents=allstudents.items, next_url=next_url,
                           prev_url=prev_url)




@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('showall'))
    if request.method == 'POST':
        Email = request.form.get('email').lower()
        input_password = request.form.get('password')
        Faculty_data = Faculty.query.filter_by(Email=Email).first()
        if Faculty_data and Faculty_data.check_password(input_password):
            login_user(Faculty_data,remember=True)
            flash(f"Welcome {Faculty_data.name}")
            return redirect(url_for("showall"))
        else:
            flash("Invalid Credentials")
            return render_template("Faculty_login.html")


    return render_template("Faculty_login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))


# homepage
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('showall'))
    if request.method == 'POST':
        if request.form.get('facultysignup'):
            return render_template("Faculty_Signup.html")
        elif request.form.get('getresult'):
            return render_template("getotp.html")
        elif request.form.get('facultylogin'):
            return render_template("Faculty_login.html")
    return render_template('homepage.html')





# new Faculty page
@app.route('/signupfaculty', methods=['GET', 'POST'])
def add_faculty():
    if current_user.is_authenticated():
        return redirect(url_for('showall'))
    if request.method == 'POST':
        try:
            name = request.form.get("name").capitalize()
            Email = request.form.get('email').lower()
            password = request.form.get('password')
            Faculty_data = Faculty.query.filter_by(Email=Email).first()
            if Faculty_data:
                flash("sorry this email is already is taken")
                return render_template("Faculty_Signup.html")
            addfaculty = Faculty(name=name, Email=Email)
            addfaculty.set_password(password)
            db.session.add(addfaculty)
            db.session.commit()
            flash("Faculty Added")
            return render_template("homepage.html")
        except exc.IntegrityError as e:
            flash("Sorry please input valid data")
            return render_template("Faculty_Signup.html")

    return render_template("Faculty_Signup.html")




@app.route('/addstudent', methods=['GET', 'POST'])
@login_required
def addstudent():
    if request.method == 'POST':
        try:
            seatno = request.form.get('seat_no')
            name = request.form.get('name').capitalize()
            Email = request.form.get('Email').lower()
            Phone = request.form.get('Phone')
            english = request.form.get('English')
            science = request.form.get('Science')
            maths = request.form.get('Maths')
            history = request.form.get('History')
            IT = request.form.get('IT')
            check_seat_no = Students.query.filter_by(seat_no=seatno).first()
            if check_seat_no:
                flash('this seat no is already been allocated ')
                return redirect(url_for("addstudent"))

            check_Phone = Students.query.filter_by(phone_no=Phone).first()
            if check_Phone:
                flash('this Phone no is already been used ')
                return redirect(url_for("addstudent"))
            check_email = Students.query.filter_by(Email=Email).first()
            if check_email:
                flash('this email is already been used ')
                return redirect(url_for("addstudent"))
            add_student = Students(seat_no=seatno, Name=name, Email=Email, phone_no=Phone, english=english,
                                   science=science, maths=maths, history=history,
                                   IT=IT)
            db.session.add(add_student)
            db.session.commit()
            flash("Student Added")
            return redirect(url_for("showall"))
        except exc.IntegrityError as e:
            flash("Sorry please input valid data")
            return redirect(url_for("addstudent"))
    return render_template("addstudent.html")


@app.route('/getotp', methods=['GET', 'POST'])
def get_otp():
    if request.method == 'POST':
        user_seatno = request.form.get('get_seatno')
        student_data = Students.query.filter_by(seat_no=user_seatno).first()
        if student_data :
            final_otp = send_otp(student_data)
            session['student'] = user_seatno
            session['otp'] = final_otp
            return redirect(url_for("submitotp"))
        else:
            flash("This seat no is invalid please try again")
            return render_template("getotp.html")
    return render_template("getotp.html")

# Student submit otp for result
@app.route('/submit', methods=['GET', 'POST'])
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
@app.route('/emailresult', methods=['GET', 'POST'])
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

# to Dele the student record
@app.route("/delete/<seat_no>",methods=['GET', 'POST'])
@login_required
def delete(seat_no):
    if current_user.is_authenticated():
        student= Students.query.filter_by(seat_no=seat_no).first()
        db.session.delete(student)
        db.session.commit()
        flash("student data Deleted successfully")
        return redirect(url_for("showall"))



@app.route("/done",methods=["GET", "POST"])
def addall():

    first_names = ['abhishek', 'rohit', 'ayush', 'karan', 'shubham', 'karan', 'pankaj', 'saurabh', 'abhijeet', 'siddhant','siddesh',
                   'pritam', 'piyush']

    last_names = ['patil', 'shinde', 'jadhav', 'sawant', 'yadav', 'joshi', 'pawar', 'gada', 'bhide']

    number = 845862412

    for i in range(4, 50):
        first_name = random.choice(first_names).capitalize()
        last_name = random.choice(last_names).capitalize()
        email_name = first_name+"."+last_name
        name = first_name+' '+last_name
        email = (f"{email_name}{i}@gmail.com").lower()
        phone = number + i

        english = random.randint(35, 99)
        science = random.randint(35, 99)
        maths = random.randint(35, 99)
        history = random.randint(35, 99)
        IT = random.randint(35, 99)

        add_student = Students(seat_no=i, Name=name, Email=email, phone_no=phone, english=english,
                               science=science, maths=maths, history=history,
                               IT=IT)
        db.session.add(add_student)
        db.session.commit()

    return "done"