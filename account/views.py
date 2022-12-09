from . import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status, views
from rest_framework.request import Request
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .emails import send_account_verification_email
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi


User = get_user_model()


class AuthUserAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserRegisterSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({'user': serializer.data})


class RegisterAPIView(CreateAPIView):
    model = get_user_model()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_account_verification_email(user, request, 'account/verify-email/')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    model = get_user_model()
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmailView(views.APIView):
    serializer_class = serializers.EmailVerificationSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        email = request.GET.get('email')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.email_verified:
                user.email_verified = True
                user.save()
            
            # TODO: Redirect
            return Response({'message': 'Email successfully verified.'}, status=status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError as e:
            user = User.objects.get(email=email)
            if user:
                send_account_verification_email(user, request, "account/verify-email/")
            return Response({'message': "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'message': 'Token is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
