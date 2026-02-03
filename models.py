from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

class Member(db.Model, UserMixin):

    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):

        self.password = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password, password)

class Profile(db.Model):

    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id', name='profile_member_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)

class PlanDetails(db.Model):
    __tablename__ = 'plan_details'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  
    price = db.Column(db.Float, nullable=False)  
    description = db.Column(db.String(200), nullable=True)  
    duration_days = db.Column(db.Integer, nullable=False)

class Payments(db.Model):

    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id', name='payments_member_id'), nullable=False)
    plan_name = db.Column(db.String(50), db.ForeignKey('plan_details.name', name='payments_plan_name'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    expiry_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending') 
    method = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f"<Payments(id={self.id}, amount={self.amount}, status={self.status})>"

