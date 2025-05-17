from datetime import datetime, timedelta, timezone
from flask import flash, g, jsonify, session, url_for,render_template,request,redirect,make_response
from flasktodo.forms import LoginForm, RegistrationForm
from flasktodo.models import Todo, User
from flasktodo import app,db,bycrpt
from flasktodo import jwt
from flask_jwt_extended import create_access_token, create_refresh_token, get_csrf_token, get_jwt,jwt_required,get_jwt_identity,set_access_cookies, set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request
from flasktodo import exception_handling
# from flasktodo.todo_page.todo import todo

# app.register_blueprint(todo,url_prefix="/Todo_Page") Working on it


@app.after_request
def check_access_expiry(response):
    print(response)
    try:
        expire_time = get_jwt()["exp"]
        print(expire_time)
        now =  datetime.now(timezone.utc)
        print(now)
        target_timestamp = datetime.timestamp(now + timedelta(seconds=10))
        if target_timestamp > expire_time:
            # Implicitly issue a new access token
            new_token = create_access_token(
                identity=get_jwt_identity(),
                fresh=False,
                expires_delta=timedelta(minutes=1)  # New expiry period
            )
            set_access_cookies(response,new_token)
        return response
    except(RuntimeError,KeyError):
        return response

@app.route("/home",methods=["GET","POST"])
@jwt_required(refresh=True)
def home():
    flash(f'Hello, Welcome Back!',category="success")
    current_user=get_jwt_identity()
    user=User().query.filter_by(email=str(current_user)).first()
    csrf_access_token = request.cookies.get('csrf_access_token')
    print(csrf_access_token)
    csrf_refresh_token = request.cookies.get('csrf_refresh_token')
    print(csrf_refresh_token)
    todo_lists=Todo.query.filter_by(user_id=user.id)
    return render_template("todo.html",todo_lists=todo_lists,csrf_access_token=csrf_access_token,csrf_refresh_token=csrf_refresh_token),200

@app.route("/add",methods=["GET","POST"])
@jwt_required(refresh=True)
def add():
    title=request.form.get("title") # Fetch the title
    user=User.query.filter_by(email=get_jwt_identity()).first()
    new_todo=Todo(title=title,status=False,user_id=user.id) # Make the table, add the values
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home")) # Send (merge) it to the Home page

@app.route("/update_status/<int:todo_id>") #kind fo like adding a parameter of int type
@jwt_required(refresh=True)
def update_status(todo_id):
    updated_todo=Todo.query.filter_by(id=todo_id).first()
    updated_todo.status= not updated_todo.status
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit/<int:todo_id>",methods=["GET","POST"])
@jwt_required(refresh=True)
def edit(todo_id):
    new_title=request.form['title']
    print(new_title)
    edited_todo=Todo.query.filter_by(id=todo_id).first()
    print(edited_todo)
    edited_todo.title=new_title
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
@jwt_required(refresh=True)
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



@app.route("/change_password",methods=["GET","POST"])
@jwt_required(fresh=True)
def change_pass():
    pass

@app.route("/",methods=["GET"])
@app.route("/login",methods=["POST","GET"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(email=form.email.data).first()
        if user and bycrpt.check_password_hash(user.password,form.password.data):
            access_token=create_access_token(identity=form.email.data,fresh=True)
            refresh_token = create_refresh_token(identity=form.email.data)
            resp=make_response(redirect('/home'))
            set_access_cookies(resp,access_token)
            set_refresh_cookies(resp,refresh_token)
            return resp
        else:
            flash(f'Re-Check Password or User Email',category="info")
    return render_template("login.html",title="Login",form=form)

@app.route('/logout',methods=['GET'])
def logout():
    resp=make_response(redirect('/login'))
    unset_jwt_cookies(resp)
    return resp,200