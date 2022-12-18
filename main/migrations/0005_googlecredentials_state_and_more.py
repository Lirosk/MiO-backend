# Generated by Django 4.1 on 2022-12-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_googlecredentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlecredentials',
            name='state',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='googlecredentials',
            name='client_id',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='googlecredentials',
            name='client_secret',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='googlecredentials',
            name='refresh_token',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='googlecredentials',
            name='scopes',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='googlecredentials',
            name='token',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='googlecredentials',
            name='token_uri',
            field=models.TextField(null=True),
        ),
    ]
