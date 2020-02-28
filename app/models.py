from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    meetings = db.relationship('Meetings', backref='manager', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_start = db.Column(db.Integer, index=True)
    time_end = db.Column(db.Integer, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey(user.id))
    client_comment = db.Column(db.String(255))
    manager_comment = db.Column(db.String(255))


    def __repr__(self):
        return '<Post {}>'.format(self.body)
