from functools import wraps
from flask import flash, redirect, render_template,Blueprint, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasktodo import db
from flasktodo.models import Todo, User

todo=Blueprint('todo',__name__,static_folder='static',template_folder='templates')

def require_jwt(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated

@todo.before_request
@require_jwt
def before_request():
    pass

@todo.route("/")
@todo.route("/home",methods=["GET","POST"])
def todo_page():
    flash(f'Hello, Welcome Back!',category="success")
    current_user=get_jwt_identity()
    user=User().query.filter_by(email=str(current_user)).first()
    csrf_token = request.cookies.get('csrf_access_token')
    todo_lists=Todo.query.filter_by(user_id=user.id)
    return render_template("todo.html",todo_lists=todo_lists,csrf_token=csrf_token),200

@todo.route("/add",methods=["GET","POST"])
def add():
    title=request.form.get("title") # Fetch the title
    user=User.query.filter_by(email=get_jwt_identity()).first()
    new_todo=Todo(title=title,status=False,user_id=user.id) # Make the table, add the values
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home")) # Send (merge) it to the Home page

@todo.route("/update_status/<int:todo_id>") #kind fo like adding a parameter of int type
def update_status(todo_id):
    updated_todo=Todo.query.filter_by(id=todo_id).first()
    updated_todo.status= not updated_todo.status
    db.session.commit()
    return redirect(url_for("home"))

@todo.route("/edit/<int:todo_id>",methods=["GET","POST"]) #kind fo like adding a parameter of int type
def edit(todo_id):
    new_title=request.form['title']
    print(new_title)
    edited_todo=Todo.query.filter_by(id=todo_id).first()
    print(edited_todo)
    edited_todo.title=new_title
    db.session.commit()
    return redirect(url_for("home"))

@todo.route("/delete/<int:todo_id>")
def delete(todo_id):
    deleting_todo=Todo.query.filter_by(id=todo_id).first()
    db.session.delete(deleting_todo)
    db.session.commit()
    return redirect(url_for("home"))
