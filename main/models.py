from django.db import models
from utils.models import TrackingModel
from django.utils.translation import gettext_lazy as _
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password


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
    connected_social_networks = models.IntegerField(
        default=0
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
                "exp": (datetime.utcnow() + timedelta(hours=1))
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return token


class CalendarEvent(TrackingModel):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=64)
    description = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_all_day = models.BooleanField()
    following_id = models.CharField(max_length=126, null=True)
    guid = models.CharField(max_length=126, null=True)
    location = models.CharField(max_length=126,null=True)
    recurrence_exception = models.CharField(max_length=128,null=True)
    recurrence_id = models.IntegerField(null=True)
    recurrence_rule = models.CharField(max_length=126,null=True)
    start_timezone = models.CharField(max_length=126,null=True)
    end_timezone = models.CharField(max_length=126, null=True)


class KanbanCategory(models.Model):
    name = models.CharField(
        max_length=32,
    )
    order = models.IntegerField(null=True)


class KanbanEvent(TrackingModel):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        KanbanCategory,
        on_delete=models.CASCADE,
    )
    description = models.TextField()


class SocialNetwork(models.Model):
    name = models.TextField(unique=True)


class ContentType(models.Model):
    name = models.TextField()
    

class StatisticMetric(models.Model):
    name = models.TextField()


class MetricValue(models.Model):
    value = models.IntegerField()
    on_date = models.DateField()


class UserToSocialNetwork(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.DO_NOTHING)


class SocialNetworkToStatisticMetric(models.Model):
    social_network = models.OneToOneField(SocialNetwork, on_delete=models.CASCADE)
    user_metric = models.ForeignKey(StatisticMetric, on_delete=models.DO_NOTHING)


class SocialNetworkToContentType(models.Model):
    social_network = models.OneToOneField(SocialNetwork, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)


class StatisticMetricToMetricValue(models.Model):
    statistic_metric = models.OneToOneField(StatisticMetric, on_delete=models.CASCADE)
    metric_value = models.ForeignKey(MetricValue, on_delete=models.DO_NOTHING)


class GoogleCredentials(TrackingModel):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE
    )
    state = models.TextField(null=True)
    token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    token_uri = models.TextField(null=True)
    client_id = models.TextField(null=True)
    client_secret = models.TextField(null=True)
    scopes = models.TextField(null=True)
    redirect_after_login = models.TextField(null=True)

    @classmethod
    def create_update(cls, *, instance=None, user=None, **kwargs):
        credentials = None
        if instance is not None and isinstance(instance, cls):
            credentials = instance
        elif user is not None:
            credentials = cls.objects.filter(user=user)
            if not credentials.exists():
                credentials = cls(user=user, **kwargs)
                credentials.save()
                return credentials

            credentials = credentials.first()
        
        for attr, value in kwargs.items(): 
            setattr(credentials, attr, value)

        credentials.save()
        return credentials


class TikTokCredentials(TrackingModel):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE
    )
    redirect_after_login = models.TextField(null=True)