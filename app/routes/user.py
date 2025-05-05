from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models import User, Inventory
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('user.html', user=user)
    flash('Будь ласка, увійдіть або зареєструйтесь', 'error')
    return redirect(url_for('auth.login'))

@user_bp.route('/add_tugriks', methods=['POST'])
def add_tugriks():
    user_id = session.get('user_id')
    if not user_id:
        flash('Будь ласка, увійдіть або зареєструйтесь', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    amount = int(request.form.get('tugriksAmount'))
    if 1 <= amount <= 1000:
        user.tugriks += amount
        db.session.commit()
        flash('Тугрики додано', 'success')
    else:
        flash('Кількість має бути від 1 до 1000', 'error')
    return redirect(url_for('user.profile'))

@user_bp.route('/inventory')
def inventory():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    items = Inventory.query.filter_by(user_id=user_id).all()
    user = User.query.get(user_id)
    return render_template('inventory.html', inventory=items, user=user)

@user_bp.route('/api/get_balance', methods=['GET'])
def get_balance():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'balance': user.tugriks})