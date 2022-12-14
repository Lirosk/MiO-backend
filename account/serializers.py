from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    redirect_to = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'redirect_to')
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
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'token', )

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

        return super().validate(user)


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        fields = ["token", "email"]


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    redirect_to = serializers.CharField(write_only=True)

    class Meta:
        fields = ['email', 'redirect_to']

    def validate(self, attrs):
        email = attrs.get('email')
        redirect_to = attrs.get('redirect_to')

        try:
            user = User.objects.get(email=email)
            if not user.email_verified:
                raise ValidationError('Email is not validated.')

            user.redirect_to = redirect_to
            user.save()
        except User.DoesNotExist as e:
            raise ValidationError('User with given email does not exists.')

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(password)
                user.save()
                return super().validate(attrs)
            
        except Exception as e:
            ...

        raise AuthenticationFailed("Reset password credentials are invalid.", 400)