from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    tugriks = db.Column(db.Integer, default=0)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), nullable=False)

    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
