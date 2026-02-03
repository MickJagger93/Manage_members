import os
from flask import Blueprint, render_template, redirect, url_for, flash, get_flashed_messages, current_app
from models import db, Payments, PlanDetails
from flask_login import login_required, current_user
from datetime import datetime, timezone
from forms import CreditCardForm, BankTransferForm, UnsubscribeForm
from sqlalchemy import func
from werkzeug.utils import secure_filename
from utils import check_subscription_reminder, can_subscribe

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    
    check_subscription_reminder()
    return render_template('layout/partials/dashboard.html')

@admin_bp.route('/subscription_options')
@login_required
def subscription():
    
    return render_template('layout/partials/subscription_opt.html')

@admin_bp.route('/payment_options/<plan_name>', methods=['GET', 'POST'])
@login_required
def payment_options(plan_name):
    
    messages = get_flashed_messages()
    plan = PlanDetails.query.filter(func.lower(PlanDetails.name) == plan_name.lower()).first()

    if not plan:
        
        flash("Invalid or unspecified plan.")
        return redirect(url_for('admin.subscription'))
    
    return render_template('layout/partials/payment_options.html', plan=plan, messages=messages)

@admin_bp.route('/bank_transfer/<plan_name>', methods=['GET', 'POST'])
@login_required
def bank_transfer(plan_name):
    
    messages = get_flashed_messages()
    form = BankTransferForm()
    
    plan = PlanDetails.query.filter(func.lower(PlanDetails.name) == plan_name.lower()).first()
    if not plan:
        flash("Invalid plan.")
        return redirect(url_for('admin.subscription'))

    can_sub, msg = can_subscribe(current_user.id, plan)
    if not can_sub:
        flash(msg)
        return redirect(url_for('admin.subscription'))

    if form.validate_on_submit():
        
        receipt_file = form.receipt.data
        filename = secure_filename(receipt_file.filename)
        
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads/') 
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        receipt_file.save(filepath)
        
        payment = Payments(
            member_id=current_user.id,
            plan_name=plan.name,
            amount=form.amount_transferred.data,
            status='Pending',
            date=datetime.now(timezone.utc),
            method='Bank Transfer')  
        
        db.session.add(payment)
        db.session.commit()

        flash('Transfer receipt uploaded and payment registered with pending status.')
        return redirect(url_for('admin.payment_receipt', payment_id=payment.id))
    
    return render_template('layout/partials/bank_transfer.html', form=form, plan=plan, messages=messages)

@admin_bp.route('/credit_card/<plan_name>', methods=['GET', 'POST'])
@login_required
def credit_card(plan_name):
    
    messages = get_flashed_messages()
    plan = PlanDetails.query.filter(func.lower(PlanDetails.name) == plan_name.lower()).first()
    if not plan:
        flash('Invalid plan.')
        return redirect(url_for('admin.subscription'))

    can_sub, msg = can_subscribe(current_user.id, plan)
    if not can_sub:
        flash(msg)
        return redirect(url_for('admin.subscription'))

    form = CreditCardForm()

    if form.validate_on_submit():
        
        payment = Payments(
            member_id=current_user.id,
            plan_name=plan.name,
            amount=plan.price,
            status='Pending',
            date=datetime.now(timezone.utc),
            method='Credit Card')
        
        db.session.add(payment)
        db.session.commit()

        flash('Card payment registered correctly.')
        return redirect(url_for('admin.payment_receipt', payment_id=payment.id))

    return render_template('layout/partials/credit_card.html', form=form, plan=plan, messages=messages)

@admin_bp.route('/payment_receipt/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def payment_receipt(payment_id):
    
    messages = get_flashed_messages()
    payment = Payments.query.get(payment_id)
    
    if not payment or payment.member_id != current_user.id:
    
        flash("Payment not found or not authorized.")
        return redirect(url_for('admin.dashboard'))
    
    return render_template('layout/partials/payment_receipt.html', payment=payment, messages=messages)

@admin_bp.route('/payment_history', methods=['GET', 'POST'])
@login_required
def payment_history():
    
    payments = Payments.query.filter_by(member_id=current_user.id).order_by(Payments.expiry_date.desc()).all()
    
    return render_template('layout/partials/payment_history.html', payments=payments)

@admin_bp.route('/view_plans', methods=['GET', 'POST'])
@login_required
def view_plans():

    form = UnsubscribeForm()
    
    messages = get_flashed_messages()
    payment = Payments.query.filter_by(member_id=current_user.id, is_active=True).first()

    return render_template('layout/partials/view_plans.html', payment=payment, form=form, messages=messages)

@admin_bp.route('/unsubscribe/<int:payment_id>', methods=['POST'])
@login_required
def unsubscribe(payment_id):
    
    payment = Payments.query.filter_by(id=payment_id, member_id=current_user.id, is_active=True).first()
    if not payment:
        flash("Subscription not found or already inactive.", "warning")
        return redirect(url_for('admin.view_plans'))

    payment.is_active = False
    payment.status = 'Cancelled'
    db.session.commit()

    flash("You have successfully unsubscribed from the plan.", "success")
    return redirect(url_for('admin.view_plans'))

