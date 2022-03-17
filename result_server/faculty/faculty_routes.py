
from flask import redirect, url_for, flash, request, render_template
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import exc

from . import faculty_app
from ..models import Faculty, Students
from .. import db


@faculty_app.route("/delete/<seat_no>", methods=['GET', 'POST'])
@login_required
def delete(seat_no):
    if current_user.is_authenticated:
        student = Students.query.filter_by(seat_no=seat_no).first()
        db.session.delete(student)
        db.session.commit()
        flash("student data Deleted successfully")
        return redirect(url_for("faculty_app.showall"))


"""paginate this route"""


# To show ALL THE STUNDENTS DATA TO THE Faculty after login
@faculty_app.route('/show', methods=['GET', 'POST'])
@login_required
def showall():
    page = request.args.get('page', 1, type=int)
    allstudents = Students.query.paginate(
        page, 10, False)
    if request.method == 'POST':
        if request.form.get('Add student'):
            return redirect(url_for("faculty_app.addstudent"))
        elif request.form.get('Logout'):
            return redirect(url_for('logout'))
    next_url = url_for('showall', page=allstudents.next_num) \
        if allstudents.has_next else None
    prev_url = url_for('showall', page=allstudents.prev_num) \
        if allstudents.has_prev else None
    return render_template("allstudents.html", allstudents=allstudents.items, next_url=next_url,
                           prev_url=prev_url)


@faculty_app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('showall'))
    if request.method == 'POST':
        Email = request.form.get('email').lower()
        input_password = request.form.get('password')
        Faculty_data = Faculty.query.filter_by(Email=Email).first()
        if Faculty_data and Faculty_data.check_password(input_password):
            login_user(Faculty_data, remember=True)
            flash(f"Welcome {Faculty_data.name}")
            return redirect(url_for("faculty_app.showall"))
        else:
            flash("Invalid Credentials")
            return render_template("Faculty_login.html")

    return render_template("Faculty_login.html")


@faculty_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))


# new Faculty page
@faculty_app.route('/signupfaculty', methods=['GET', 'POST'])
def add_faculty():
    if current_user.is_authenticated:
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


@faculty_app.route('/addstudent', methods=['GET', 'POST'])
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
                return redirect(url_for("faculty_app.addstudent"))

            check_Phone = Students.query.filter_by(phone_no=Phone).first()
            if check_Phone:
                flash('this Phone no is already been used ')
                return redirect(url_for("faculty_app.addstudent"))
            check_email = Students.query.filter_by(Email=Email).first()
            if check_email:
                flash('this email is already been used ')
                return redirect(url_for("faculty_app.addstudent"))
            add_student = Students(seat_no=seatno, Name=name, Email=Email, phone_no=Phone, english=english,
                                   science=science, maths=maths, history=history,
                                   IT=IT)
            db.session.add(add_student)
            db.session.commit()
            flash("Student Added")
            return redirect(url_for("faculty_app.showall"))
        except exc.IntegrityError as e:
            flash("Sorry please input valid data")
            return redirect(url_for("faculty_app.addstudent"))
    return render_template("addstudent.html")
