from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Redirect(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    after_email_verification = models.TextField()
    after_password_reset = models.TextField(null=True)