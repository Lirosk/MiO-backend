# Generated by Django 4.1 on 2022-12-18 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_kanbancategory_kanbanevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('token_uri', models.TextField()),
                ('client_id', models.TextField()),
                ('client_secret', models.TextField()),
                ('scopes', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
