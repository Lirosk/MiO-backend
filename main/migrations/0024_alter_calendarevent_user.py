# Generated by Django 4.1 on 2022-12-16 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_calendarevent_description_calendarevent_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
