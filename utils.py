import re
from wtforms import ValidationError
from flask import flash
from models import Payments
from flask_login import current_user
from datetime import datetime, timezone, timedelta
from models import PlanDetails, db
from sqlalchemy import func

def check_subscription_reminder():
    
    active_plan = Payments.query.filter_by(member_id=current_user.id, is_active=True).first()
    if active_plan and active_plan.expiry_date:
        days_left = (active_plan.expiry_date - datetime.now(timezone.utc)).days
        if 0 < days_left <= 3:
            flash(f'Reminder: You have {days_left} days to renew your subscription ({active_plan.plan}).', 'warning')

def strong_password(form, field):
    password = field.data
    
    if len(re.findall(r'[0-9]', password)) < 2:
        raise ValidationError('Password must contain at least 2 numbers.')
    if len(re.findall(r'[A-Za-z]', password)) < 2:
        raise ValidationError('Password must contain at least 2 letters.')
    if len(re.findall(r'[^A-Za-z0-9]', password)) < 2:
        raise ValidationError('Password must contain at least 2 special characters.')

def seed_plan_details():
    
        if PlanDetails.query.first():
            
            return

        plans = [
            PlanDetails(name='weekly', price=9.99, description='Plan semanal', duration_days=7),
            PlanDetails(name='monthly', price=29.99, description='Plan mensual', duration_days=30),
            PlanDetails(name='annual', price=299.99, description='Plan anual', duration_days=365),
        ]

        for plan in plans:
            db.session.add(plan)
        db.session.commit()

def can_subscribe(user_id, new_plan):
    
    active_payment = Payments.query.filter(
        Payments.member_id == user_id,
        Payments.status.in_(['Pending', 'Active'])
    ).order_by(Payments.date.desc()).first()
    
    if not active_payment:
        return True, None
    
    current_plan = PlanDetails.query.filter(func.lower(PlanDetails.name) == active_payment.plan_name.lower()).first()
    if not current_plan or not hasattr(current_plan, 'duration_days'):
        return False, "You already have an active or pending subscription. Please cancel it before subscribing to a new plan."
    
    from datetime import timezone, datetime, timedelta

    active_date_aware = active_payment.date.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    subscription_end_date = active_date_aware + timedelta(days=current_plan.duration_days)
    
    if now < subscription_end_date:
        return False, f"You currently have an active subscription for plan '{active_payment.plan_name}'. Please wait until {subscription_end_date.strftime('%Y-%m-%d')} to subscribe to a new plan."
    
    return True, None
