from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    containers = db.relationship('Container', backref='user', lazy=True)

class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.String(64), unique=True)
    port = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))