from rest_framework import serializers
from . import models


class KanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        exclude = ["created_at", "updated_at"]
        extra_kwargs = {
            "id": {
                "read_only": False
            },
            "user": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        id = attrs.get("id", 0)
        user = attrs.get("user", None)
        existing = models.KanbanEvent.objects.filter(id=id, user=user)
        if not existing.exists():
            raise serializers.ValidationError("Kanban event with given id doesn't exists.", 400)

        return super().validate(attrs)


class PutKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        exclude = ["created_at", "updated_at"]
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


class KanbanCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanCategory
        fields = '__all__'


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        exclude = ["created_at", "updated_at"]
        extra_kwargs = {
            "id": {
                "read_only": False
            },
            "user": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        id = attrs.get("id", 0)
        user = attrs.get("user", None)
        existing = models.CalendarEvent.objects.filter(id=id, user=user)
        if not existing.exists():
            raise serializers.ValidationError("Calendar event with given id doesn't exists.", 400)

        return super().validate(attrs)


class PutCalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        exclude = ["created_at", "updated_at"]


class DeleteCalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        fields = ["id", "user"]
        extra_kwargs = {
            "id": {
                "read_only": False
            },
            "user": {
                "write_only": True
            }
        }