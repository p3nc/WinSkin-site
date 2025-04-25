from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.mainpage'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('main.mainpage'))
        else:
            flash('Неправильний логін або пароль', 'error')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if 'user_id' in session:
        return redirect(url_for('main.mainpage'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if password != confirm_password:
            flash('Паролі не збігаються', 'error')
            return redirect(url_for('auth.registration'))

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Користувач із таким логіном або email вже існує', 'error')
            return redirect(url_for('auth.registration'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Реєстрація пройшла успішно!', 'success')
        return redirect(url_for('main.mainpage'))
    return render_template('registration.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
