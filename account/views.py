from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.request import Request
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from . import serializers


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

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    model = get_user_model()
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        