# Generated by Django 4.1 on 2022-12-18 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_googlecredentials_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanbancategory',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
