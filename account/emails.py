from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()
EMAIL_FROM = settings.EMAIL_HOST

def send_account_verification_email(user, request, relative_link):
    token = user.email_verification_token
    current_site = get_current_site(request).domain
    abs_url = f"http://{current_site}/{relative_link}?token={str(token)}&email={user.email}"

    subject = "MiO Email Verification"
    message = f"To verify you email, please go to the following link:\n.{abs_url}"
    sent_count = send_mail(subject, message, EMAIL_FROM, [user.email])

    if sent_count == 0:
        raise Exception('Email isn\'t sent.')
    
def send_password_reset_email(user, request, relative_link):
    current_site = get_current_site(request).domain

    abs_url = f"http://{current_site}/{relative_link}"

    subject = "MiO Password Reset"
    message = f"To reset your password, please use the link below:\n{abs_url}"

    send_mail(subject, message, EMAIL_FROM, [user.email])