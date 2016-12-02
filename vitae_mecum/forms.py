from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, PasswordField, DateField
from models import db, User, JournalEntry


class ContactForm(Form):
    name = StringField("Name", [validators.InputRequired("Please enter your name.")])
    email = StringField("Email", [validators.InputRequired("Please enter your email."), validators.Email("Please enter "
                        "a valid email address.")])
    subject = StringField("Subject", [validators.InputRequired("Please enter the subject.")])
    message = TextAreaField("Message", [validators.InputRequired("Please enter your message.")])
    submit = SubmitField("Send")


class SignupForm(Form):
    firstname = StringField("First name",  [validators.InputRequired("Please enter your first name.")])
    lastname = StringField("Last name",  [validators.InputRequired("Please enter your last name.")])
    email = StringField("Email",  [validators.InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.InputRequired("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email = StringField("Email",  [validators.InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.InputRequired("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False


class JournalForm(Form):
    entry = TextAreaField("Entry", [validators.InputRequired("Please enter your entry.")])  # SEE IF POSSIBLE TO HAVE WYSIWIG FIELD
    date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        entry = JournalEntry.query.filter_by(date=self.date.data).first()
        if entry is not None:
            self.date.errors.append("Journal entry already exists")
            return False
        return True
