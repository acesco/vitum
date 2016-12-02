__author__ = 'Benjamin'

from flask import Flask

app = Flask(__name__)

app.secret_key = 'insert secret key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'username'
app.config["MAIL_PASSWORD"] = 'password'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bhbritta:periodic@bhbritta.mysql.pythonanywhere-services.com/' \
                                        'bhbritta$vitum'

from vitae_mecum.models import db
db.init_app(app)

from vitae_mecum.routes import mail
mail.init_app(app)

import vitae_mecum.routes