# Generated by Django 4.1 on 2022-12-17 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='subscription',
            field=models.CharField(max_length=36, null=True),
        ),
    ]
