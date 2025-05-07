from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField

class RegistrationForm(FlaskForm):
    email = StringField('Email address')
    password=PasswordField('Password')
    submit_btn=SubmitField('Sign Up!')
class LoginForm(FlaskForm):
    email = StringField('Email address')
    password=PasswordField('Password')
    submit_btn=SubmitField('Sign in!')