# Generated by Django 4.1 on 2022-12-14 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_rename_kanbancategories_kanbancategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kanbancategory',
            name='name',
        ),
        migrations.RemoveField(
            model_name='kanbanevent',
            name='category',
        ),
        migrations.RemoveField(
            model_name='kanbanevent',
            name='description',
        ),
        migrations.RemoveField(
            model_name='kanbanevent',
            name='user',
        ),
    ]
