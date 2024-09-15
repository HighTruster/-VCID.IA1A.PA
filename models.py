from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    birthday = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    vms = db.relationship('VM', backref='author', lazy=True)

class VM(db.Model):
    __tablename__ = 'VM'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cpu = db.Column(db.Integer, nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    hdd = db.Column(db.Integer, nullable=False)
    ipv4 = db.Column(db.String(16), unique=True, nullable=False)  # String length adjusted to match varchar(16)
    mac = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)