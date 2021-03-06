# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)
db = SQLAlchemy(app)

import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER, ADMINS,
                               'Candela - blad:', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)



lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = u"Aby załadować tę stronę musisz być zalogowany!"



from app import views, models
