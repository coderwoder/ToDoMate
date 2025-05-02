from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Tracks modifications to the database and send signals when change occurs

db = SQLAlchemy(app)

from flasktodo import routes