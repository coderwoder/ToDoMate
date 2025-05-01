from flask import Flask,url_for,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Tracks modifications to the database and send signals when change occurs

db = SQLAlchemy(app)

class Todo(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150))
    status=db.Column(db.Boolean)

@app.route("/")
def home():
    todo_lists=Todo.query.all()
    return render_template("index.html",todo_lists=todo_lists)

@app.route("/add",methods=["POST"])
def add():
    title=request.form.get("title") # Fetch the title
    new_todo=Todo(title=title,status=False) # Make the table, add the values
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home")) # Send (merge) it to the Home page

@app.route("/update_status/<int:todo_id>") #kind fo like adding a parameter of int type
def update_status(todo_id):
    updated_todo=Todo.query.filter_by(id=todo_id).first()
    updated_todo.status= not updated_todo.status
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
    db.drop_all()