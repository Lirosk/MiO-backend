import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from rest_framework import exceptions
import os
from google.oauth2.credentials import Credentials
import pathlib
from datetime import datetime, date
from . import models
from .serializers import GoogleCredentialsSerializer
dir_path = pathlib.Path(__file__).parent.resolve()


class Google:
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

    @property
    @classmethod
    def scope(cls):
        return ",".join(cls.SCOPES)

    @classmethod
    def fetch(cls, request):
        code = request.GET["code"]
        cls.flow.fetch_token(code=code)
        credentials = cls.flow.credentials

        state = request.GET["state"]
        saved_credentials = models.GoogleCredentials.objects.filter(
            state=state)
        if not saved_credentials.exists():
            raise exceptions.APIException("Invalid credentials", 400)

        saved_credentials = saved_credentials.first()
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
    def revoke_token(cls, request):
        requests.post('https://oauth2.googleapis.com/revoke',
                      params={'token': request.session["credentials"].token},
                      headers={'content-type': 'application/x-www-form-urlencoded'})

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
        start_date = start_date or f"{now.year-1}-{now.month}-{'01' if (period == 'day') else now.day}"
        end_date = end_date or f"{now.year}-{now.month}-{'01' if (period == 'day') else now.day}"

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
    def user(cls, user, *, metric=None, period=None, start_date=None, end_date=None):
        youtubeAnalytics = cls.get_analytics_service(user)
        period, start_date, end_date = cls.define_period_and_dates(
            period, start_date, end_date)

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

        return formatted_result.values()

    @classmethod
    def get(cls, user):
        return {}

    @classmethod
    def content_type(cls, user, *, content_type=None, metric=None, period=None, start_date=None, end_date=None):
        youtube = cls.get_data_service(user)

        res = cls.execute_api_request(
            youtube
        )

        return []


available = {"youtube": Google}
