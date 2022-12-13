from django.utils import timezone
from django.apps import apps
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from utils.models import TrackingModel


class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        username = extra_fields.pop(
            'username') if 'username' in extra_fields else ''
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, username=username, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        primary_key=True,
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        null=True,
        unique=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    email_verified = models.BooleanField(
        _("email_verified"),
        default=False,
        help_text=_(
            "Designates whether this users email should is verified."
        ),
    )
    redirect_to = models.CharField(
        _("redirect_to"),
        max_length=126,
        default="",
        help_text=_(
            "Url redirect to after email verification and password reset."
        ),
    )

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def token(self):
        token = jwt.encode(
            {
                'email': self.email,
                'exp': (datetime.utcnow() + timedelta(hours=24))
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return token

    @property
    def email_verification_token(self):
        token = jwt.encode({
                'email': self.email,
                'user_id': self.id,
                "exp": (datetime.utcnow() + timedelta(hours=1))
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return token


class CalendarEvent(models.Model):
    ...


class KanbanCategories(models.Model):
    ...


class KanbanEvent(models.Model):
    ...


class SocialNetwork(models.Model):
    ...


class ContentType(models.Model):
    ...


class StatisticMetric(models.Model):
    ...


class MetricValue(models.Model):
    ...
