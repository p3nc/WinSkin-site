from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Отримуємо абсолютний шлях до директорії проекту
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

# Використовуємо абсолютний шлях для бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "db.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

# Модель користувача
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    tugriks = db.Column(db.Integer, default=0)

migrate = Migrate(app, db)

@app.route('/')
def index():
    return redirect(url_for('mainpage'))

@app.route('/roulette')
def roulette():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('roulette.html', user=user)

@app.route('/mainpage')
def mainpage():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('mainpage.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('mainpage'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('mainpage'))
        else:
            flash('Неправильний логін або пароль', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if 'user_id' in session:
        return redirect(url_for('mainpage'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if password != confirm_password:
            flash('Паролі не збігаються', 'error')
            return redirect(url_for('registration'))

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Користувач із таким логіном або email вже існує', 'error')
            return redirect(url_for('registration'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація пройшла успішно!', 'success')
        session['user_id'] = new_user.id
        return redirect(url_for('mainpage'))
    return render_template('registration.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/user')
def user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('user.html', user=user)
    flash('Будь ласка, увійдіть або зареєструйтесь', 'error')
    return redirect(url_for('login'))

@app.route('/add_tugriks', methods=['POST'])
def add_tugriks():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            tugriks_amount = int(request.form.get('tugriksAmount'))
            if 1 <= tugriks_amount <= 1000:
                if user.tugriks is None:
                    user.tugriks = 0
                user.tugriks += tugriks_amount
                db.session.commit()
                flash('Тугрики успішно додані!', 'success')
            else:
                flash('Кількість тугриків повинна бути від 1 до 1000', 'error')
        else:
            flash('Користувач не знайдений', 'error')
    else:
        flash('Будь ласка, увійдіть або зареєструйтесь', 'error')
    return redirect(url_for('user'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)