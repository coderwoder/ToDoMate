from flasktodo import db
class Todo(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150))
    status=db.Column(db.Boolean)