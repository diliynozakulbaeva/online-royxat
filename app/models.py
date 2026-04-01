from .database import db
from datetime import datetime
import random

class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(1), unique=True, nullable=False)
    tickets = db.relationship('Ticket', backref='branch', lazy=True)

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, default=10)
    tickets = db.relationship('Ticket', backref='service', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(10), unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    status = db.Column(db.String(20), default='waiting')  # waiting, called, done
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_number(branch_code):
        suffix = random.randint(100, 999)
        existing = {t.ticket_number for t in Ticket.query.all()}
        number = f"{branch_code}-{suffix}"
        while number in existing:
            suffix = random.randint(100, 999)
            number = f"{branch_code}-{suffix}"
        return number