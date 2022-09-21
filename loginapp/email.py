from flask_mail import Message
from . import mail
from flask import render_template, current_app


def send_email(subject, to, txt_body, html_body=None, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=app.config["MAIL_SUBJECT_PREFIX"]+subject,
                  recipients=[to],
                  sender=app.config["MAIL_SENDER"])
    msg.body = render_template(txt_body, **kwargs)
    mail.send(msg)
