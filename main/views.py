from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . import serializers
from . import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

def add_user_to_request_data_list_items( request):
    try:
        for data in request.data:
            data["user"] = request.user.email
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
        events = models.KanbanEvent.objects.filter(user=request.user)
        serialized = serializers.KanbanSerializer(events, many=True)
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
        serialized.save()
        return Response(serialized.data, status=status.HTTP_200_OK)

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
        for obj in serialized.validated_data:
            event = models.KanbanEvent.objects.get(id=obj["id"])
            event.category = obj["category"]
            event.description = obj["description"]
            event.save()

        return Response(serialized.data, status=status.HTTP_200_OK)

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
        add_user_to_request_data_list_items(request)
        serialized = serializers.DeleteKanbanSerializer(data=request.data, many=True)
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
        categories = models.KanbanCategory.objects.all()
        serialized = self.serializer_class(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class CalendarAPIView(APIView):
    def get(self, request):
        events = models.CalendarEvent.objects.filter(user=request.user)
        serialized = serializers.CalendarEventSerializer(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.PutCalendarEventSerializer(request.data, many=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.CalendarEventSerializer(data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        for obj in serialized.validated_data:
            event = models.CalendarEvent.objects.get(id=obj["id"])
            event_serialized = serializers.CalendarEventSerializer(data=event)
            event_serialized.update(event, obj)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        add_user_to_request_data_list_items(request)
        serialized = serializers.DeleteCalendarEventSerializer(data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        for obj in serialized.validated_data:
            existing = models.CalendarEvent.objects.filter(**obj, user=request.user)
            if not existing.exists():
                return Response({"message": "Calendar event with given id doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
            existing.first().delete()

        return Response(serialized.data, status=status.HTTP_200_OK)