# Generated by Django 4.1 on 2022-12-16 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_kanbanevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='end_timezone',
            field=models.CharField(max_length=126, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='following_id',
            field=models.CharField(max_length=126, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='guid',
            field=models.CharField(max_length=126, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='is_all_day',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='location',
            field=models.CharField(max_length=126, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='recurrence_exception',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='recurrence_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='recurrence_rule',
            field=models.CharField(max_length=126, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='start_timezone',
            field=models.CharField(max_length=126, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='subject',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]