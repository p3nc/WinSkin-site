from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from app import db
from app.email import send_registration_email

auth_bp = Blueprint('auth', __name__, url_prefix='')


@auth_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if 'user_id' in session:
        return redirect(url_for('main.mainpage'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.registration'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.registration'))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        send_registration_email(user)
        flash('Registration successful! Please check your email.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('registration.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.mainpage'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('main.mainpage'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
