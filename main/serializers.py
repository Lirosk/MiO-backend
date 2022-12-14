from rest_framework import serializers
from . import models

class KanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        fields = ["id", "category", "description"]