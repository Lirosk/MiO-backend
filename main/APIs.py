import requests
from rest_framework import exceptions
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import os
from google.oauth2.credentials import Credentials
import pathlib
from datetime import datetime, date
from . import models
from .serializers import GoogleCredentialsSerializer
from utils import utils
from oauthlib.oauth2.rfc6749 import errors

dir_path = pathlib.Path(__file__).parent.resolve()


class API:
    @classmethod
    def name(cls):
        return cls.__name__

    @classmethod
    def db_connect_user(cls, user):
        s = models.SocialNetwork.objects.filter(name=cls.name())
        if not s.exists():
            return

        s = s.first()
        us = models.UserToSocialNetwork.objects.filter(user=user, social_network=s)
        if not us.exists():
            models.UserToSocialNetwork(user=user, social_network=s).save()


    @classmethod
    def db_disconnect_user(cls, user):
        s = models.SocialNetwork.objects.filter(name=cls.name())
        if not s.exists():
            return

        s = s.first()
        us = models.UserToSocialNetwork.objects.filter(user=user, social_network=s)
        if us.exists():
            us.delete()


    @classmethod
    def authorize(cls, user, redirect_url): ...

    @classmethod
    def authorized(cls, request): ...

    @classmethod
    def cancel(cls, user):
        cls.db_disconnect_user(user)

    @classmethod
    def is_user_authorized(cls, user): ...

    @classmethod
    def save_metric_value(cls, user, content_type_name, metric_name, metric_value, metric_date):
        social_network_name = cls.name()
        user_to_social_network = models.SocialNetwork.objects.get(name=social_network_name)
        user_to_social_network = models.UserToSocialNetwork.objects.filter(user=user, social_network=user_to_social_network)
        if user_to_social_network.exists():
            user_to_social_network = user_to_social_network.first()
        else:
            user_to_social_network = models.UserToSocialNetwork(user=user, social_network=user_to_social_network)
            user_to_social_network.save()

        on_date = datetime.fromisoformat(metric_date)

        user_to_social_network
        if content_type_name == "user":
            statistic_metric = models.StatisticMetric.objects.filter(name=metric_name)
            if statistic_metric.exists():
                statistic_metric = statistic_metric.first()
            else:
                statistic_metric = models.StatisticMetric(name=metric_name)
                statistic_metric.save()
            
            social_network_to_statistic_metric = models.SocialNetworkToStatisticMetric.objects.filter(social_network=user_to_social_network, user_metric=statistic_metric)
            if social_network_to_statistic_metric.exists():
                social_network_to_statistic_metric = social_network_to_statistic_metric.first()
            else:
                social_network_to_statistic_metric = models.SocialNetworkToStatisticMetric(social_network=user_to_social_network, user_metric=statistic_metric)
                social_network_to_statistic_metric.save()

            statistic_metric_to_metric_value = models.StatisticMetricToMetricValue.objects.filter(statistic_metric=social_network_to_statistic_metric)
            if statistic_metric_to_metric_value.exists():
                related = [*statistic_metric_to_metric_value.select_related().all()]
                for found in related:
                    metric_value = found.metric_value
                    if metric_value.on_date == on_date:
                        metric_value.value = metric_value
                        metric_value.save()
            else:
                metric_value = models.MetricValue(value=metric_value, on_date=metric_date)
                metric_value.save()

                statistic_metric_to_metric_value = models.StatisticMetricToMetricValue(statistic_metric=social_network_to_statistic_metric, metric_value=metric_value)
                statistic_metric_to_metric_value.save()

        return


class YouTube(API):
    SCOPES = [
        "https://www.googleapis.com/auth/yt-analytics.readonly",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]
    ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
    ANALYTICS_API_VERSION = "v2"

    DATA_API_SERVICE_NAME = "youtube"
    DATA_API_VERSION = "v3"

    USER_METRICS = ["views", "likes", "comments", "dislikes",
                    "shares", "subscribersGained", "subscribersLost"]

    secrets_file = os.path.join(
        dir_path.parent.absolute(), "client_secret.json")

    flow = Flow.from_client_secrets_file(
        secrets_file,
        SCOPES
    )

    @classmethod
    def get_authorization_url(cls, redirect_url):
        cls.flow.redirect_uri = f"{redirect_url}"
        return cls.flow.authorization_url()

    @classmethod
    def scope(cls):
        return ",".join(cls.SCOPES)

    @classmethod
    def fetch(cls, request):
        if "code" not in request.GET:
            raise exceptions.APIException("Invalid credentials.", 400)

        code = request.GET["code"]
        state = request.GET["state"]

        credentials = ...

        try:
            # flow = Flow.from_client_secrets_file(cls.secrets_file, cls.SCOPES, state=state)
            flow = cls.flow
            # flow.redirect_uri = "http://localhost/oauth2callback"
            flow.fetch_token(code=code)
            credentials = flow.credentials
        except errors.InvalidGrantError:
            raise exceptions.APIException("Invalid credentials", 400)
        
        saved_credentials = models.GoogleCredentials.objects.filter(
            state=state)
        if not saved_credentials.exists():
            raise exceptions.APIException("Invalid credentials", 400)

        saved_credentials = saved_credentials.first()

        user = saved_credentials.user

        cls.db_connect_user(user)

        if not saved_credentials.token and not utils.can_user_connect_more_social_networks(user):
            raise exceptions.APIException("This user can't connect more social networks.")

        if not saved_credentials.token:
            user.connected_social_networks += 1
            user.save()

        res_credentials = models.GoogleCredentials.create_update(
            instance=saved_credentials,
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes="+".join(credentials.scopes),
        )
        return res_credentials

    @classmethod
    def revoke_token(cls, credentials):
        requests.post('https://oauth2.googleapis.com/revoke',
                      params={'token': credentials.token},
                      headers={'content-type': 'application/x-www-form-urlencoded'})

    @classmethod
    def cancel(cls, user):
        super().cancel(user)
        credentials = models.GoogleCredentials.objects.filter(user=user).first()
        if not credentials.token:
            credentials.delete()
            return
        credentials.user.connected_social_networks -= 1
        credentials.user.save()
        cls.revoke_token(credentials)
        credentials.delete()

    @classmethod
    def is_user_authorized(cls, user):
        google_credentials = models.GoogleCredentials.objects.filter(user=user)
        if not google_credentials.exists():
            return False

        google_credentials = google_credentials.first()
        return bool(google_credentials.client_id)


    @classmethod
    def execute_api_request(cls, client_library_function, **kwargs):
        response = client_library_function(
            **kwargs
        ).execute()
        return response

    @classmethod
    def get_service(cls, service_name, api_version, credentials):
        return build(service_name, api_version, credentials=credentials)

    @classmethod
    def get_credentials(cls, user):
        google_credentials = models.GoogleCredentials.objects.filter(user=user)
        if not google_credentials.exists():
            raise exceptions.APIException(
                "Login to social network first.", 400)

        google_credentials = google_credentials.first()

        if not google_credentials.client_id:
            raise exceptions.APIException(
                "Login to social network first.", 400)

        serializer = GoogleCredentialsSerializer(google_credentials)
        info = {**serializer.data}
        info["scopes"] = info["scopes"].split("+")

        credentials = Credentials(**info)
        return credentials

    @classmethod
    def get_analytics_service(cls, user):
        credentials = cls.get_credentials(user)
        service = cls.get_service(cls.ANALYTICS_API_SERVICE_NAME, cls.ANALYTICS_API_VERSION, credentials)
        return service

    @classmethod
    def get_data_service(cls, user):
        credentials = cls.get_credentials(user)
        service = cls.get_service(cls.DATA_API_SERVICE_NAME, cls.DATA_API_VERSION, credentials=credentials)
        return service

    @classmethod
    def define_period_and_dates(cls, period, start_date, end_date):
        now = datetime.now()

        period = period or "month"
        start_date = start_date or f"{now.year-1 if period == 'month' else now.year}-{now.month -1 if period=='day' else now.month}-{'01' if (period == 'month') else now.day}"
        end_date = end_date or f"{now.year}-{now.month}-{'01' if (period == 'month') else now.day}"

        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        if start > end:
            start_date, end_date = end_date, start_date

        if start_date and period == "month":
            start_date = start_date[:-2] + '01'

        if end_date and period == "month":
            end_date = end_date[:-2] + '01'

        return period, start_date, end_date


    @classmethod
    def authorize(cls, user, redirect_after_login):
        auth_url, state = cls.get_authorization_url(f"https://c8eb-46-53-253-96.eu.ngrok.io/statistics/youtube/authorized/")
        models.GoogleCredentials.create_update(user=user, state=state, redirect_after_login=redirect_after_login)
        print(f"{user.email}: {auth_url=}")
        return auth_url

    @classmethod
    def authorized(cls, request):
        return cls.fetch(request).redirect_after_login


    @classmethod
    def user(cls, user, *, metric=None, period=None, start_date=None, end_date=None):
        # if not start_date:
        #     youtube = cls.get_data_service(user)
        #     s = youtube.channels().list("statistics", mine=True)

        youtubeAnalytics = cls.get_analytics_service(user)

        period, start_date, end_date = cls.define_period_and_dates(
            period, start_date, end_date
        )

        res = cls.execute_api_request(
            youtubeAnalytics.reports().query,
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics=metric or ",".join(cls.USER_METRICS),
            dimensions=period or "day",
            sort=period or "day"
        )

        formatted_result = {}

        on_date_index = 0

        for (i, metric) in enumerate(res["columnHeaders"]):
            name = metric["name"]
            if name == period:
                on_date_index = i
                continue

            formatted_result[name] = {}
            formatted_result[name]["name"] = name.lower()
            formatted_result[name]["values"] = []

        for row in res["rows"]:
            on_date = row[on_date_index]

            for (i, metric) in enumerate(res["columnHeaders"]):
                if i == on_date_index:
                    continue
                formatted_result[metric["name"]]["values"].append({
                    "value": row[i],
                    "on_date": on_date
                })

                cls.save_metric_value(user, "user", metric["name"], row[i], on_date)

        return formatted_result.values()

    @classmethod
    def get(cls, user, **kwargs):
        return {
            "name": cls.name(),
            "user_metrics": cls.user(user, **kwargs)
        }

    @classmethod
    def content_type(cls, user, *, content_type=None, metric=None, period=None, start_date=None, end_date=None):
        youtube = cls.get_data_service(user)

        return []


class TikTok(API):
    @classmethod
    def authorize(cls, user, redirect_url):
        cls.db_connect_user(user)
        credentials = models.TikTokCredentials.objects.filter(user=user)
        
        if not credentials.exists() and not utils.can_user_connect_more_social_networks(user):
            raise exceptions.APIException("This user can't connect more social networks.")

        if not credentials.exists():
            models.TikTokCredentials(user=user).save()
            user.connected_social_networks += 1
            user.save()

        return redirect_url

    @classmethod
    def authorized(cls, request):
        return ""

    @classmethod
    def cancel(cls, user):
        super().cancel(user)
        user.connected_social_networks -= 1
        user.save()
        models.TikTokCredentials.objects.filter(user=user).delete()

    @classmethod
    def is_user_authorized(cls, user):
        return models.TikTokCredentials.objects.filter(user=user).exists()


available = {"youtube": YouTube, "tiktok": TikTok}