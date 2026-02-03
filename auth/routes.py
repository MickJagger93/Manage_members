from flask import Blueprint, render_template, url_for, redirect, flash, get_flashed_messages
from flask_login import login_user, logout_user
from models import Member, db
from forms import LoginForm, RegisterForm, ResetPassword

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    messages = get_flashed_messages()

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        member = Member.query.filter_by(email=email).first()

        if not member or not member.check_password(password):

            flash('Invalid email or password. Please try again.')
            return redirect(url_for('auth.login'))

        login_user(member)

        return redirect(url_for('admin.dashboard'))
    
    return render_template('layout/partials/login.html', form=form, messages=messages)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    messages = get_flashed_messages()

    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:

            flash('Password do not match. Please try again.')
            return render_template('layout/partials/register.html', form=form)

        member = Member.query.filter_by(email=email).first()

        if member:

            flash('Your email is already registered.')
            return redirect(url_for('auth.register'))

        else:

            member = Member(name=name, email=email, password=password)
            member.set_password(password)
            db.session.add(member)
            db.session.commit()

            flash('Successfully registration! Please log in.')
            return redirect(url_for('auth.login'))

    return render_template('layout/partials/register.html', form=form, messages=messages)

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    
    form = ResetPassword()
    messages = get_flashed_messages()

    if form.validate_on_submit:

        email = form.email.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if new_password == confirm_new_password:

            user = Member.query.filter_by(email=email).first()

            if user:

                user.set_password(new_password)
                db.session.commit()

                flash('Your password has been successfully updated!')
                return redirect(url_for('auth.login'))

        else:
            flash('Passwords do not match or invalid email. Please try again.')
    
    return render_template('layout/partials/reset.html', form=form, messages=messages)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    
    logout_user()
    flash('You have been logged out succesfully.')
    return redirect(url_for('auth.login'))

