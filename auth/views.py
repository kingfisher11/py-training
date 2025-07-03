from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from einvoicing import db
from einvoicing.user.models import User
from einvoicing.auth.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))

        # Create the user without password first
        user = User(
            name=form.name.data,
            email=form.email.data
        )

        # Set hashed password
        user.set_password(form.password.data)

        # Add and commit to DB
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email

            flash('Login successful!', 'success')
            return redirect(url_for('student.list_student'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
