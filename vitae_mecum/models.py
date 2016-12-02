from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    date = db.Column(db.Date, primary_key=True)
    entry = db.Column(db.Text, nullable=False)

    def __init__(self, uid, date, entry):
        self.uid = uid
        self.date = date
        self.entry = entry


class Goal(db.Model):
    __tablename__ = 'goals'
    gid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)  # FOREIGN KEY REFERENCE
    year = None  # INCOMPLETE
    description = None  # INCOMPLETE
    time_frame = None  # INCOMPLETE

    def __init__(self, uid, year, description, time_frame):
        self.gid = self.setGID(uid)
        self.year = year
        self.description = description
        self.time_frame = time_frame

    def setGID(self, uid):
        pass
