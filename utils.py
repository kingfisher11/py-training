from functools import wraps
from flask import session, redirect, url_for, flash
from flask_mail import Message
from flask import render_template
from einvoicing import mail, db
from einvoicing.user.models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def send_student_created_email(student):
    users = User.query.all()
    with mail.connect() as conn:
        for user in users:
            msg = Message(subject='📘 New Student Registered',
                          recipients=[user.email])
            msg.body = render_template('emails/student_created.txt', student=student)
            msg.html = render_template('emails/student_created.html', student=student)
            conn.send(msg)