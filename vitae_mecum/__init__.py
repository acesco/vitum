__author__ = 'Benjamin'

from flask import Flask

app = Flask(__name__)

app.secret_key = 'insert secret key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'username'
app.config["MAIL_PASSWORD"] = 'password'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/' \
                                        'vitum'

from models import db
db.init_app(app)

from routes import mail
mail.init_app(app)

import vitae_mecum.routes