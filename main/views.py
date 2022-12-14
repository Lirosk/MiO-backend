from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . import serializers
from . import models


# Create your views here.

class KanbanAPIView(GenericAPIView):
    serializer_class = serializers.KanbanSerializer

    def get(self, request):
        events = models.KanbanEvent.objects.filter(user=request.user)
        serialized = self.serializer_class(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


    def put(self, request):
        ...

    def patch(self, request):
        ...

    def delete(self, request):
        ...

