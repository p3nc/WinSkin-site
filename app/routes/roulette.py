from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from app.models import User, Skin, Inventory
from app import db

roulette_bp = Blueprint('roulette', __name__, url_prefix='/roulette')

@roulette_bp.route('/')
def roulette():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template('roulette.html', user=user)

@roulette_bp.route('/spin', methods=['POST'])
def spin():
    user = User.query.get(session.get('user_id'))
    if not user:
        return {'error': 'Unauthorized'}, 401
    if user.tugriks < 100:
        return {'error': 'Недостатньо тугриків'}, 400

    user.tugriks -= 100
    db.session.commit()

    return {'success': True, 'tugriks': user.tugriks}

@roulette_bp.route('/save', methods=['POST'])
def save():
    user = User.query.get(session.get('user_id'))
    if not user:
        return {'error': 'Unauthorized'}, 401

    data = request.get_json()
    new_skin = Inventory(
        user_id=user.id,
        skin_name=data['name'],
        rarity=data['rarity'],
        image=data['image']
    )
    db.session.add(new_skin)
    db.session.commit()
    return {'success': True}

@roulette_bp.route('/get_skins/<collection>')
def get_skins(collection):
    skins = Skin.query.filter_by(collection=collection).all()
    return jsonify({
        'skins': [{
            'name': s.name,
            'rarity': s.rarity,
            'photo': s.photo
        } for s in skins]
    })
