# Generated by Django 4.1 on 2022-12-14 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_delete_kanbancategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='KanbanEvent',
        ),
    ]
