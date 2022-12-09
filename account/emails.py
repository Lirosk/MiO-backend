from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()
EMAIL_FROM = settings.EMAIL_HOST

def send_account_verification_email(user, request, relative_link):
    # token = RefreshToken.for_user(user).access_token
    token = user.email_verification_token
    current_site = get_current_site(request).domain
    # relative_link = reverse(redirect_to_view)

    subject = "MiO Email Verification"
    message = f"To verify you email, please go to the following link:\nhttp://{current_site}/{relative_link}?token={str(token)}&email={user.email}."
    sent_count = send_mail(subject, message, EMAIL_FROM, [user.email])

    if sent_count == 0:
        raise Exception('Email isn\'t sent.')
    