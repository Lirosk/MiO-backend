from django.db import models
from datetime import datetime

# Create your models here.

class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-created_at', )