from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(Form):
    name = StringField("Name", [validators.InputRequired("Please enter your name.")])
    email = StringField("Email", [validators.InputRequired("Please enter your email."), validators.Email("Please enter "
                        "a valid email address.")])
    subject = StringField("Subject", [validators.InputRequired("Please enter the subject.")])
    message = TextAreaField("Message", [validators.InputRequired("Please enter your message.")])
    submit = SubmitField("Send")