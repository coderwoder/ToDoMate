from flask import jsonify, session, url_for,render_template,request,redirect
from flasktodo.forms import LoginForm, RegistrationForm
from flasktodo.models import Todo, User
from flasktodo import app,db
from flasktodo import jwt
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity

@app.route("/",methods=["GET"])
@jwt_required()
def home():
    current_user=get_jwt_identity()
    print(current_user)
    todo_lists=Todo.query.all()
    return render_template("todo.html",todo_lists=todo_lists),200

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

@app.route("/register",methods=["POST","GET"])
def register():
    form =RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # print(User.query.all())
        return redirect(url_for('login'))
    return render_template("register.html",title="Register",form=form)

@app.route("/login",methods=["POST","GET"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        # print(user)
        if form.email.data!='Admin123' and form.password.data!='passwork':
            print("Rong passwork")
        else:
            access_token=create_access_token(identity=form.email.data)
            return redirect(url_for("home")) 
    return render_template("login.html",title="Login",form=form)