# Generated by Django 4.1 on 2022-12-12 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0008_productpricefeature_remove_pricetoproduct_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductPriceFeature',
        ),
    ]