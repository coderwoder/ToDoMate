from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email,EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email address')
    password=PasswordField('Password')
    confirm_password=PasswordField("Confirm Password",validators=[EqualTo("password")])
    submit_btn=SubmitField('Sign Up!')
class LoginForm(FlaskForm):
    email = StringField('Email address')
    password=PasswordField('Password')
    submit_btn=SubmitField('Sign in!')