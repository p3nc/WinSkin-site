from flask import Blueprint, redirect, url_for, render_template, session
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('main.mainpage'))

@main_bp.route('/mainpage')
def mainpage():
    user = User.query.get(session.get('user_id')) if 'user_id' in session else None
    return render_template('mainpage.html', user=user)
