from flask import url_for,render_template,request,redirect
from flasktodo.models import Todo
from flasktodo import app,db
@app.route("/")
def home():
    todo_lists=Todo.query.all()
    return render_template("todo.html",todo_lists=todo_lists)

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

@app.route("/edit/<int:todo_id>",methods=["POST"])
def edit(todo_id):
    new_title=request.form['title']
    print(new_title)
    edited_todo=Todo.query.filter_by(id=todo_id).first()
    print(edited_todo)
    edited_todo.title=new_title
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    deleting_todo=Todo.query.filter_by(id=todo_id).first()
    db.session.delete(deleting_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/register")
def register():
    return render_template("register.html",title="Register")

@app.route("/login")
def login():
    return render_template("login.html",title="Login")