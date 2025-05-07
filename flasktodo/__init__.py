from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app= Flask(__name__)

app.config['SECRET_KEY']='SECRET'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
app.config['JWT_SECRET_KEY']='jwt_secret'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt =JWTManager(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Tracks modifications to the database and send signals when change occurs

db = SQLAlchemy(app)

from flasktodo import routes