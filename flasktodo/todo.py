from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Tracks modifications to the database and send signals when change occurs

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/add")
# def add():


if __name__ == '__main__':
    app.run(debug=True)