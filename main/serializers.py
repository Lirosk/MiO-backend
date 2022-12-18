from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


User = get_user_model()


class KanbanCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanCategory
        fields = '__all__'


class KanbanSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    category = serializers.CharField()

    class Meta:
        model = models.KanbanEvent
        exclude = ["created_at", "updated_at", "user"]
        extra_kwargs = {
            "id": {
                "read_only": False
            },
        }

    def validate(self, attrs):
        id = attrs.get("id", 0)
        email = attrs.get("email", "")
        user = User.objects.get(email=email)
        existing = models.KanbanEvent.objects.filter(id=id, user=user)
        if not existing.exists():
            raise serializers.ValidationError("Kanban event with given id doesn't exists.", 400)
        
        existing_category = models.KanbanCategory.objects.filter(name=attrs["category"])
        if not existing_category.exists():
            raise serializers.ValidationError("Given kanban category doesn't exists", 400)

        attrs["category"] = existing_category.first()
        return super().validate(attrs)


class PutKanbanSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = models.KanbanEvent
        fields = ["id", "category", "description"]
        extra_kwargs = {
            "id": {
                "read_only": True
            }
        }

    def validate(self, attrs):
        category_name = attrs.get("category")
        category = models.KanbanCategory.objects.filter(name=category_name)
        if not category.exists():
            raise serializers.ValidationError("Give kanban category doesn't exists.")

        attrs["category"] = category.first()

        return super().validate(attrs)

    def create(self, validated_data):
        email = validated_data.pop("email")
        user = User.objects.get(email=email)

        category_name = validated_data.pop("category")
        category = models.KanbanCategory.objects.get(name=category_name)

        event = models.KanbanEvent(**validated_data, user=user, category=category)
        event.save()
        return event


class WriteKanbanSerializer(serializers.ModelSerializer):
    category = KanbanCategorySerializer()

    class Meta:
        model = models.KanbanEvent
        fields = ["id", "category", "description"]


class DeleteKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KanbanEvent
        fields = ["id"]
        extra_kwargs = {
            "id": {
                "read_only": False
            }
        }


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        exclude = ["created_at", "updated_at", "user"]
        extra_kwargs = {
            "id": {
                "read_only": False
            },
        }

    def validate(self, attrs):
        id = attrs.get("id", 0)
        existing = models.CalendarEvent.objects.filter(id=id)
        if not existing.exists():
            raise serializers.ValidationError("Calendar event with given id doesn't exists.", 400)

        return super().validate(attrs)


class PutCalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        exclude = ["created_at", "updated_at", "user"]
        extra_kwargs = {
        }

    def validate(self, attrs):
        

        return super().validate(attrs)


class DeleteCalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        fields = ["id"]
        extra_kwargs = {
            "id": {
                "read_only": False
            },
        }

    def validate(self, attrs):
        id = attrs.get("id", 0)

        existing = models.CalendarEvent.objects.filter(id=id)
        if not existing.exists():
            raise serializers.ValidationError("Calendar event doesn't exists.")

        return super().validate(attrs)