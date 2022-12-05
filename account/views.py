from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.request import Request
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from . import serializers


User = get_user_model()

# class LoginView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]

#     def get(self, request: HttpRequest, format=None):
#         if request.method != 'GET':
#             return HttpResponseBadRequest()

#         content = {
#             'username': str(request.GET['username']),
#             'password': str(request.GET['password']),
#         }

#         user = authenticate(**content)

#         if user is None:
#             return HttpResponseBadRequest()

#         return Response(user is not None)


class RegisterView(CreateAPIView):
    model = get_user_model()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
