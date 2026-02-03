from flask import Blueprint, flash, get_flashed_messages, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from forms import ProfileForm
from models import db, Profile

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    messages = get_flashed_messages()
    profile = Profile.query.filter_by(member_id=current_user.id).first()
    
    if profile is None:
        flash("You have no profile information. Please complete your profile.")
        return redirect(url_for('user.edit_profile', member_id=current_user.id))
    
    return render_template('layout/partials/profile.html', profile=profile, messages=messages)

@user_bp.route('/edit_profile/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(member_id):
    
    profile = Profile.query.filter_by(member_id=member_id).first()
    
    if profile is None:
        profile = Profile(member_id=member_id)

    form = ProfileForm(request.form, obj=profile)

    if form.validate_on_submit():
        form.populate_obj(profile)
        db.session.add(profile)
        db.session.commit()
        flash('Information correctly updated.')
        return redirect(url_for('user.profile'))

    return render_template('layout/partials/edit_profile.html', form=form, profile=profile)

@user_bp.route('/delete_profile/<int:member_id>', methods=['POST'])
@login_required
def delete_profile(member_id):
    
    if request.method == 'POST':
    
        profile = Profile.query.filter_by(member_id=member_id).first_or_404()

        db.session.delete(profile)
        db.session.commit()
        flash('Your information profile has been deleted.')
    
    return redirect(url_for('admin.subscription'))