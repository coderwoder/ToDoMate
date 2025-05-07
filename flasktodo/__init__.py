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
app.config['JWT_ACCESS_COOKIE_PATH']='/'
app.config['JWT_COOKIE_CSRF_PROTECT']=True

jwt =JWTManager(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Tracks modifications to the database and send signals when change occurs

db = SQLAlchemy(app)

from flasktodo import routes