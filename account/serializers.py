from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed


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

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        return super().validate(attrs)


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

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = authenticate(email=email, password=password) 

        if not user:
            raise AuthenticationFailed('Invalid credentials.')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled.')
        if not user.email_verified:
            raise AuthenticationFailed('Email is not verified.')

        return super().validate(attrs)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model=User
        fields = ['token'] 