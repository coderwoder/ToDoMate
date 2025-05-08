from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, ValidationError
from wtforms.validators import Email,EqualTo,DataRequired,Length
from flasktodo.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email address',
                        validators=[DataRequired(),Email()])
    password=PasswordField('Password',
                           validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField("Confirm Password",
                                   validators=[EqualTo("password")])
    submit_btn=SubmitField('Sign Up!')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This Email Already Exist, Try another one...")


class LoginForm(FlaskForm):
    email = StringField('Email address',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit_btn=SubmitField('Sign in!')