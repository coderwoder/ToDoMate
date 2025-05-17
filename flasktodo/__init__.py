from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app= Flask(__name__)
bycrpt= Bcrypt(app)
# login_manager=LoginManager(app)

app.config['SECRET_KEY']='SECRET'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"

app.config['JWT_SECRET_KEY']='jwt_secret'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURITY'] =False

app.config['JWT_REFRESH_CSRF_FIELD_NAME'] = 'csrf_refresh_token' # Tell it the name of your refresh CSRF token field
app.config['JWT_ACCESS_CSRF_FIELD_NAME'] = 'csrf_access_token'
app.config['JWT_ACCESS_COOKIE_PATH']='/'
app.config['JWT_REFRESH_COOKIE_PATH']='/'

app.config['JWT_COOKIE_CSRF_PROTECT']=True
app.config['JWT_CSRF_CHECK_FORM']=True

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] =timedelta(minutes=5)

jwt =JWTManager(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Tracks modifications to the database and send signals when change occurs

db = SQLAlchemy(app)

from flasktodo import routes
