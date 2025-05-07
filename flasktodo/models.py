from flasktodo import db

class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),nullable=False,unique=True)
    password=db.Column(db.String(20),nullable=False)
    todo_list = db.relationship('Todo', backref="list")

    def __repr__(self):
        return f"User=({self.email})"

class Todo(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150))
    status=db.Column(db.Boolean)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Todo=({self.title},{self.status})"