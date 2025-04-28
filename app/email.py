from flask_mail import Message
from app import mail
from flask import current_app


def send_registration_email(user):
    msg = Message('Welcome to WinSkin!',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])

    msg.body = f'''Hi {user.username},

Welcome to WinSkin! Your registration was successful.

Thank you for joining us!'''

    mail.send(msg)