from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


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
    admin = db.Column(db.Boolean, nullable=False, default=False)

# Модель скіна
class Skin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50), nullable=False)
    collection = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(100), nullable=False)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skin_name = db.Column(db.String(100), nullable=False)
    rarity = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    date_obtained = db.Column(db.DateTime, default=db.func.current_timestamp())


migrate = Migrate(app, db)

from functools import wraps
from flask import abort


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user = User.query.get(session['user_id'])
        if not user or not user.admin:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


@app.route('/admin/skins', methods=['GET', 'POST'])
@admin_required
def admin_skins():
    if request.method == 'POST':
        try:
            new_skin = Skin(
                name=request.form['name'],
                rarity=request.form['rarity'],
                collection=request.form['collection'],
                photo=request.form['photo']
            )
            db.session.add(new_skin)
            db.session.commit()
            flash('Skin added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding skin', 'error')
            print(f"Error: {e}")

        return redirect(url_for('admin_skins'))

    skins = Skin.query.all()
    return render_template('admin_skins.html', skins=skins)


@app.route('/admin/skins/delete/<int:skin_id>', methods=['POST'])
@admin_required
def delete_skin(skin_id):
    try:
        skin = Skin.query.get_or_404(skin_id)
        db.session.delete(skin)
        db.session.commit()
        flash('Skin deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting skin', 'error')
        print(f"Error: {e}")

    return redirect(url_for('admin_skins'))


# Add error handler for 403 errors
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
@app.route('/')
def index():
    return redirect(url_for('mainpage'))

@app.route('/roulette')
def roulette():
    if 'user_id' not in session:
        return redirect(url_for('login'))
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

@app.route('/spin_roulette', methods=['POST'])
def spin_roulette():
    if 'user_id' not in session:
        return {'error': 'Потрібно увійти в систему'}, 401

    user = User.query.get(session['user_id'])
    if not user:
        return {'error': 'Користувача не знайдено'}, 404

    if user.tugriks < 100:
        return {'error': 'Недостатньо тугриків'}, 400

    user.tugriks -= 100
    db.session.commit()

    return {'success': True, 'tugriks': user.tugriks}


@app.route('/save_won_skin', methods=['POST'])
def save_won_skin():
    if 'user_id' not in session:
        return {'error': 'Потрібно увійти в систему'}, 401

    data = request.get_json()
    user = User.query.get(session['user_id'])

    new_skin = Inventory(
        user_id=user.id,
        skin_name=data['name'],
        rarity=data['rarity'],
        image=data['image']
    )

    db.session.add(new_skin)
    db.session.commit()

    return {'success': True}


@app.route('/get_case_skins/<collection>')
def get_case_skins(collection):
    skins = Skin.query.filter_by(collection=collection).all()
    return jsonify({
        'skins': [{
            'name': skin.name,
            'rarity': skin.rarity,
            'photo': skin.photo
        } for skin in skins]
    })


@app.route('/inventory')
def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    inventory_items = Inventory.query.filter_by(user_id=user_id).all()

    return render_template('inventory.html', inventory=inventory_items, user=user)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)