# Generated by Django 4.1 on 2022-12-14 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_productpricefeature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='per_unit',
            field=models.IntegerField(),
        ),
    ]