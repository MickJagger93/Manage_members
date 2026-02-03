from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, validators, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from utils import strong_password

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), strong_password])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), strong_password])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ResetPassword(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password= PasswordField('New Password', validators=[DataRequired(), strong_password])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    reset = SubmitField('Reset Password')

class ProfileForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Save')

class CreditCardForm(FlaskForm):
    
    card_number = StringField('Card Number', [validators.Optional(), validators.Length(min=16, max=16)])
    expiry_date = StringField('Expiration date (MM/YY)', [validators.Optional()])
    cvv = StringField('CVV', [validators.Optional(), validators.Length(min=3, max=3)])
    submit = SubmitField('Pay')

class BankTransferForm(FlaskForm):
    bank_used = SelectField(
        'Banco utilizado',
        choices=[('Wells Fargo', 'Wells Fargo'), ('Bank of America', 'Bank of America'), ('Otro', 'Otro Banco')],
        validators=[DataRequired()]
    )
    transfer_date = DateField('Transfer date', validators=[DataRequired()])
    amount_transferred = DecimalField('Amount transferred', validators=[DataRequired(), NumberRange(min=0.01)])
    receipt = FileField('Attach proof of payment', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Only images and PDFs are allowed.')])
    submit = SubmitField('Send receipt')

class UnsubscribeForm(FlaskForm):
    submit = SubmitField('Unsubscribe')


class DeleteProfileForm(FlaskForm):
    submit = SubmitField('Delete Information')