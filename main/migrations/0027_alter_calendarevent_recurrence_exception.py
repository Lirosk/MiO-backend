# Generated by Django 4.1 on 2022-12-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_calendarevent_options_calendarevent_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='recurrence_exception',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
