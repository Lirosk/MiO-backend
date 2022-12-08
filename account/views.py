from . import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .emails import send_account_verification_email
import jwt
from django.conf import settings

User = get_user_model()


class AuthUserAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        serializer = serializers.UserRegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(CreateAPIView):
    model = get_user_model()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        if (serializer.is_valid()):
            serializer.save()
            user = User.objects.get(email=serializer.validated_data['email'])
            try:
                send_account_verification_email(
                    user, request, 'account/verify-email/')
            except Exception as e:
                user.delete()
                return Response({'message': 'Error during sending email, check your email'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    model = get_user_model()
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    def post(self, request: Request):
        print(f'{request.content_type = }')
        print(f'{request.data = }')
        print(f'{request.POST = }')

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyEmailView(GenericAPIView):
    permission_classes = (AllowAny, )
    authentication_classes = []

    def get(self, request):
        token = request.GET.get('token')
        email = request.GET.get('email')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.email_verified:
                user.email_verified = True
                user.save()
            return Response({'message': 'Email successfully verified.'}, status=status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError as e:
            user = User.objects.get(email=email)
            if user:
                send_account_verification_email(user, request, "account/verify-email/")
            return Response({'message': "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'message': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
