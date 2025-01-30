from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citacao = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('TagNota', backref='nota', lazy=True, cascade='all, delete-orphan')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.relationship('TagNota', backref='tag', lazy=True, cascade='all, delete-orphan')

class TagNota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota_id = db.Column(db.Integer, db.ForeignKey('nota.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)