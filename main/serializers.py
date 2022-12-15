from rest_framework import serializers
from . import models


class KanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        fields = ["id", "category", "description"]


class PatchKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        fields = ["id", "category", "description", "user"]
        extra_kwargs = {
            "id": {
                "read_only": False
            }
        }

    def validate(self, attrs):
        id = attrs.get("id", 0)
        existing = models.KanbanEvent.objects.filter(id=id)
        if not existing.exists():
            raise serializers.ValidationError("Kanban event with given id doesn't exists.", 400)

        return super().validate(attrs)


class PutKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        fields = ["id", "category", "description", "user"]
        extra_kwargs = {
            "user": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        event = models.KanbanEvent(**validated_data)
        event.save()
        return event


class DeleteKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        fields = ["id"]
        extra_kwargs = {
            "id": {
                "read_only": False
            },
        }
