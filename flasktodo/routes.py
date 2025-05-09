from flask import flash, jsonify, session, url_for,render_template,request,redirect,make_response
from flasktodo.forms import LoginForm, RegistrationForm
from flasktodo.models import Todo, User
from flasktodo import app,db,bycrpt
from flasktodo import jwt
from flask_jwt_extended import create_access_token, get_csrf_token,jwt_required,get_jwt_identity,set_access_cookies, unset_jwt_cookies, verify_jwt_in_request
from flasktodo import exception_handling


@app.route("/home",methods=["GET","POST"])
@jwt_required()
def home():
    flash(f'Hello, Welcome Back!',category="success")
    current_user=get_jwt_identity()
    csrf_token = request.cookies.get('csrf_access_token')
    print(csrf_token)
    print(current_user)
    todo_lists=Todo.query.all()
    return render_template("todo.html",todo_lists=todo_lists,csrf_token=csrf_token),200

@app.route("/add",methods=["GET","POST"])
@jwt_required()
def add():
    title=request.form.get("title") # Fetch the title
    user=User.query.filter_by(email=get_jwt_identity()).first()
    new_todo=Todo(title=title,status=False,user_id=user.id) # Make the table, add the values
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home")) # Send (merge) it to the Home page

@app.route("/update_status/<int:todo_id>") #kind fo like adding a parameter of int type
@jwt_required()
def update_status(todo_id):
    updated_todo=Todo.query.filter_by(id=todo_id).first()
    updated_todo.status= not updated_todo.status
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit/<int:todo_id>",methods=["POST"])
@jwt_required()
def edit(todo_id):
    new_title=request.form['title']
    print(new_title)
    edited_todo=Todo.query.filter_by(id=todo_id).first()
    print(edited_todo)
    edited_todo.title=new_title
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
@jwt_required()
def delete(todo_id):
    deleting_todo=Todo.query.filter_by(id=todo_id).first()
    db.session.delete(deleting_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/register",methods=["POST","GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bycrpt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'User Account Created Please Sign in',category='success')
        return redirect(url_for('login'))
    return render_template("register.html",title="Register",form=form)

@app.route("/",methods=["GET"])
@app.route("/login",methods=["POST","GET"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(email=form.email.data).first()
        if user and bycrpt.check_password_hash(user.password,form.password.data):
            access_token=create_access_token(identity=form.email.data)
            resp=make_response(redirect('/home'))
            set_access_cookies(resp,access_token)
            return resp
        else:
            flash(f'Re-Check Password or User Email',category="info")
    return render_template("login.html",title="Login",form=form)

@app.route('/logout',methods=['GET'])
def logout():
    resp=make_response(redirect('/login'))
    unset_jwt_cookies(resp)
    return resp,200