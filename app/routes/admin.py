from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models import Skin, User
from app import db
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or not user.admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/skins', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.admin_skins'))

    skins = Skin.query.all()
    return render_template('admin_skins.html', skins=skins)

@admin_bp.route('/skins/delete/<int:skin_id>', methods=['POST'])
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
    return redirect(url_for('admin.admin_skins'))
