from flask import Blueprint, render_template
from sqlalchemy import func
from einvoicing import db
from einvoicing.user.models import User
from einvoicing.student.models import Student

home = Blueprint('home', __name__)

@home.route('/')
def dashboard():
    total_users = User.query.count()
    total_students = Student.query.count()

    # Students grouped by prog_code
    student_counts = (
        db.session.query(Student.prog_code, func.count(Student.id))
        .group_by(Student.prog_code)
        .all()
    )

    labels = [row[0] for row in student_counts]
    values = [row[1] for row in student_counts]

    return render_template('home/dashboard.html', total_users=total_users, total_students=total_students, labels=labels, values=values)
