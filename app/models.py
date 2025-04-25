from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    tugriks = db.Column(db.Integer, default=0)
    admin = db.Column(db.Boolean, nullable=False, default=False)

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
