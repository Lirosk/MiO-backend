# Generated by Django 4.1 on 2022-12-19 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_usertosocialnetwork_statisticmetrictometricvalue_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialnetworktocontenttype',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='socialnetworktocontenttype',
            name='user_social_network',
        ),
        migrations.RemoveField(
            model_name='socialnetworktostatisticmetric',
            name='user_metric',
        ),
        migrations.RemoveField(
            model_name='socialnetworktostatisticmetric',
            name='user_social_network',
        ),
        migrations.RemoveField(
            model_name='statisticmetrictometricvalue',
            name='metric_value',
        ),
        migrations.RemoveField(
            model_name='statisticmetrictometricvalue',
            name='statistic_metric',
        ),
        migrations.RemoveField(
            model_name='usertosocialnetwork',
            name='social_network',
        ),
        migrations.RemoveField(
            model_name='usertosocialnetwork',
            name='user',
        ),
        migrations.DeleteModel(
            name='ContentTypeToStatisticMetric',
        ),
        migrations.DeleteModel(
            name='SocialNetworkToContentType',
        ),
        migrations.DeleteModel(
            name='SocialNetworkToStatisticMetric',
        ),
        migrations.DeleteModel(
            name='StatisticMetricToMetricValue',
        ),
        migrations.DeleteModel(
            name='UserToSocialNetwork',
        ),
    ]
