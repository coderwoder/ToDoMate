from flasktodo import app
from flasktodo import db
if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
    # db.drop_all() #reset the whole todo database after server close