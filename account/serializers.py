from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 128
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'token', )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8, 'max_length': 128
            }
        }
        read_only_fields = ['token']
