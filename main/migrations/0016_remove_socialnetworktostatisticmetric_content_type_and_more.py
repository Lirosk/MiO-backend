# Generated by Django 4.1 on 2022-12-19 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_contenttype_metricvalue_socialnetwork_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialnetworktostatisticmetric',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='socialnetworktostatisticmetric',
            name='social_network',
        ),
        migrations.RemoveField(
            model_name='statisticmetrictometricvalue',
            name='metric_value',
        ),
        migrations.RemoveField(
            model_name='statisticmetrictometricvalue',
            name='statistic_metric',
        ),
        migrations.DeleteModel(
            name='ContentType',
        ),
        migrations.DeleteModel(
            name='MetricValue',
        ),
        migrations.DeleteModel(
            name='SocialNetwork',
        ),
        migrations.DeleteModel(
            name='SocialNetworkToStatisticMetric',
        ),
        migrations.DeleteModel(
            name='StatisticMetric',
        ),
        migrations.DeleteModel(
            name='StatisticMetricToMetricValue',
        ),
    ]