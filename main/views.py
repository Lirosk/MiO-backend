from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . import serializers
from . import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


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
        serialized = serializers.PatchKanbanSerializer(events, many=True)
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
        self.add_user_to_request(request)
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
        self.add_user_to_request(request)
        serialized = serializers.PatchKanbanSerializer(data=request.data, many=True)
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
        self.add_user_to_request(request)
        serialized = serializers.DeleteKanbanSerializer(data=request.data, many=True)
        serialized.is_valid(raise_exception=True)
        for obj in serialized.validated_data:
            existing = models.KanbanEvent.objects.filter(**obj, user=request.user)
            if not existing.exists():
                return Response({"message": "Kanban event with given id doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
            existing.first().delete()

        return Response(serialized.data, status=status.HTTP_200_OK)

    def add_user_to_request(self, request):
        try:
            for data in request.data:
                data["user"] = request.user.email
        except TypeError:
            return Response({"message": "Invalid data format."}, status=status.HTTP_400_BAD_REQUEST)


class KanbanCategoriesAPIView(GenericAPIView):
    serializer_class = serializers.KanbanCategorySerializer

    def get(self, request):
        categories = models.KanbanCategory.objects.all()
        serialized = self.serializer_class(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)