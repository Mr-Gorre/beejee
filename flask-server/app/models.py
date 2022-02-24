from app import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)


class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    text = db.Column(db.String(1000))
    status = db.Column(db.Boolean, default=False)
