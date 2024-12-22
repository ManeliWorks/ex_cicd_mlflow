from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    result = db.relationship("userResult", backref='author', lazy=True)

class userResult(db.Model):
    __tablename__ = "user_result"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    color = db.Column(db.String(100), nullable=False)
    cut = db.Column(db.String(100), nullable=False)
    clarity = db.Column(db.String(100), nullable=False)
    carat = db.Column(db.Float, nullable=False)
    depth = db.Column(db.Float, nullable=False)
    table = db.Column(db.Float, nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    z = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
