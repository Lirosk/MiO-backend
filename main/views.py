from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . import serializers
from . import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponseRedirect
from .import APIs

# Create your views here.


def add_user_to_request_data_list_items(request):
    try:
        for data in request.data:
            data["email"] = request.user.email
            data["user"] = request.user
    except TypeError:
        return Response({"message": "Invalid data format."}, status=status.HTTP_400_BAD_REQUEST)


class KanbanAPIView(APIView):
    id = openapi.Parameter("id", in_=openapi.IN_BODY,
                           type=openapi.TYPE_INTEGER)
    category = openapi.Parameter(
        "category", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    description = openapi.Parameter(
        "description", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[])
    def get(self, request):
        events = [*models.KanbanEvent.objects.filter(user=request.user)]
        serialized = serializers.WriteKanbanSerializer(events, many=True)
        for obj in serialized.data:
            obj["category"] = obj["category"]["name"]

        return Response(serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    'category': category,
                    'description': description,
                }
            ),
        ),
    )
    def put(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.PutKanbanSerializer(
            data=request.data, many=True)
        serialized.is_valid(raise_exception=True)

        # TODO: make this better
        saved_events = []
        for obj in serialized.validated_data:
            event = models.KanbanEvent(user=request.user, **obj)
            event.save()
            saved_events.append(event)
        
        res = serializers.WriteKanbanSerializer(saved_events, many=True)
        for obj in res.data:
            obj["category"] = obj["category"]["name"]

        return Response(
            res.data,
            status=status.HTTP_200_OK
        )


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': id,
                    'category': category,
                    'description': description,
                }
            ),
        ),
    )
    def patch(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.KanbanSerializer(data=request.data, many=True)
        serialized.is_valid(raise_exception=True)

        # TODO: make this better
        saved_events = []
        for obj in serialized.validated_data:
            event = models.KanbanEvent.objects.get(id=obj["id"])
            event.category = obj["category"]
            event.description = obj["description"]
            event.save()
            saved_events.append(event)

        res = serializers.WriteKanbanSerializer(saved_events, many=True)
        for obj in res.data:
            obj["category"] = obj["category"]["name"]

        return Response(res.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': id,
                }
            ),
        ),
    )
    def delete(self, request):
        serialized = serializers.DeleteKanbanSerializer(
            data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        for obj in serialized.validated_data:
            existing = models.KanbanEvent.objects.filter(**obj, user=request.user)
            if not existing.exists():
                return Response({"message": "Kanban event with given id doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
            existing.first().delete()

        return Response(serialized.data, status=status.HTTP_200_OK)


class KanbanCategoriesAPIView(GenericAPIView):
    serializer_class = serializers.KanbanCategorySerializer

    def get(self, request):
        categories = models.KanbanCategory.objects.all().order_by("order")
        serialized = self.serializer_class(categories, many=True)
        res = []
        for obj in serialized.data:
            res.append(obj["name"])
        return Response(res, status=status.HTTP_200_OK)


class CalendarAPIView(APIView):
    id = openapi.Parameter(
        "id", in_=openapi.IN_BODY, type=openapi.TYPE_INTEGER, required=True)
    subject = openapi.Parameter(
        "subject", in_=openapi.IN_BODY, type=openapi.TYPE_STRING, required=True)
    description = openapi.Parameter(
        "description", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    start_time = openapi.Parameter(
        "start_time", in_=openapi.IN_BODY, type=openapi.TYPE_STRING, required=True)
    end_time = openapi.Parameter(
        "end_time", in_=openapi.IN_BODY, type=openapi.TYPE_STRING, required=True)
    is_all_day = openapi.Parameter(
        "is_all_day", in_=openapi.IN_BODY, type=openapi.TYPE_BOOLEAN, required=True)
    following_id = openapi.Parameter(
        "following_id", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    guid = openapi.Parameter(
        "guid", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    location = openapi.Parameter(
        "location", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    recurrence_exception = openapi.Parameter(
        "recurrence_exception", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    recurrence_id = openapi.Parameter(
        "recurrence_id", in_=openapi.IN_BODY, type=openapi.TYPE_INTEGER)
    recurrence_rule = openapi.Parameter(
        "recurrence_rule", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    start_timezone = openapi.Parameter(
        "start_timezone", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    end_timezone = openapi.Parameter(
        "end_timezone", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[])
    def get(self, request):
        events = models.CalendarEvent.objects.filter(user=request.user)
        serialized = serializers.CalendarEventSerializer(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    "subject": subject,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                    "is_all_day": is_all_day,
                    "following_id": following_id,
                    "guid": guid,
                    "location": location,
                    "recurrence_exception": recurrence_exception,
                    "recurrence_id": recurrence_id,
                    "recurrence_rule": recurrence_rule,
                    "start_timezone": start_timezone,
                    "end_timezone": end_timezone,
                }
            )
    ))
    def put(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.PutCalendarEventSerializer(
            data=request.data, many=True)
        
        serialized.is_valid(raise_exception=True)
        for obj in serialized.validated_data:
            obj["user"] = request.user
        
        serialized.save()
        return Response(serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": id,
                    "subject": subject,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                    "is_all_day": is_all_day,
                    "following_id": following_id,
                    "guid": guid,
                    "location": location,
                    "recurrence_exception": recurrence_exception,
                    "recurrence_id": recurrence_id,
                    "recurrence_rule": recurrence_rule,
                    "start_timezone": start_timezone,
                    "end_timezone": end_timezone,
                }
            )
    ))
    def patch(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.CalendarEventSerializer(
            data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        for obj in serialized.validated_data:
            event = models.CalendarEvent.objects.filter(id=obj["id"], user=request.user)
            if not event.exists():
                raise serializers.serializers.ValidationError("Calendar with given id doesn't exists", 400)
            
            event = event.first()
            event_serialized = serializers.CalendarEventSerializer(data=event)
            event_serialized.update(event, obj)

        return Response(serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": id,
                }
            )
    ))
    def delete(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.DeleteCalendarEventSerializer(
            data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        for obj in serialized.validated_data:
            existing = models.CalendarEvent.objects.filter(**obj, user=request.user)
            if not existing.exists():
                return Response({"message": "Calendar event with given id doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
            existing.first().delete()

        return Response(serialized.data, status=status.HTTP_200_OK)


class GoogleAuthorizeAPIView(GenericAPIView):
    serializer_class = serializers.SocialNetworkAuthenticationSerializer

    @swagger_auto_schema(
        request_body=serializers.SocialNetworkAuthenticationSerializer,
        responses={
            200: openapi.Response(
                "Success",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "authorization_url": openapi.Parameter(
                            "authorization_url",
                            in_=openapi.IN_BODY,
                            type=openapi.TYPE_STRING
                        )
                    })
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        auth_url, state = APIs.Google.get_authorization_url(f"https://c8eb-46-53-253-96.eu.ngrok.io/statistics/google/authorized/")
        models.GoogleCredentials.create_update(user=request.user, state=state, redirect_after_login=serializer.validated_data["redirect_url"])
        return Response({"authorization_url": auth_url}, status=status.HTTP_200_OK)


class GoogleAuthorizedAPIView(APIView):
    authentication_classes = []

    def get(self, request):
        credentials = APIs.Google.fetch(request)
        return HttpResponseRedirect(credentials.redirect_after_login)


class SocialNetworkStatisticsAPIView(GenericAPIView):
    serializer_class = serializers.SocialNetworkStatisticsSerializer

    @swagger_auto_schema(request_body=serializers.SocialNetworkStatisticsSerializer)
    def post(self, request, social_network=None, content_type=None, metric=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        social_network = social_network.lower() or ""

        if social_network not in APIs.available:
            return Response({"message": "Unsupported social network."}, status=status.HTTP_400_BAD_REQUEST)

        api = APIs.available[social_network]

        kwargs = {}
        method = api.get

        if content_type is not None:
            if content_type.lower() == "user":
                method = api.user
            else:
                def wrapper(*args, **kwargs):
                    api.content_type(*args, **kwargs,content_type=content_type)
                method = wrapper

        res = method(request.user, metric=metric, **serializer.validated_data)

        return Response(
            res,
            status=status.HTTP_200_OK
        )