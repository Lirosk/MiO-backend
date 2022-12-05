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

class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request: HttpRequest, format=None):
        if request.method != 'GET':
            return HttpResponseBadRequest()

        content = {
            'username': str(request.GET['username']),
            'password': str(request.GET['password']),
        }

        user = authenticate(**content)

        if user is None:
            return HttpResponseBadRequest()

        return Response(user is not None)


class RegisterView(CreateAPIView):
    model = get_user_model()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny, )

    def post(self, request: HttpRequest, *args, **kwargs):
        breakpoint()

        if request.method != 'POST':
            return HttpResponseBadRequest({
                'Message': f'Method {request.method} is not acceptable.'
            })

        print(f'{request.get_full_path()}')
        print(f'{request.POST = }')
        print(f'{request.body = }')

        if 'email' not in request.POST:
            return HttpResponseBadRequest({
                'Message': f'Email field must be specified.'
            })

        if 'password' not in request.POST:
            return HttpResponseBadRequest({
                'Message': f'Password field must be specified.'
            })

        print(f'{(request.POST) = }')

        if 'username' not in request.POST:
            request.POST['username'] = request.POST['email']

        return super().post(request, *args, **kwargs)


@api_view(['POST'])
def register_view(request: Request):
    if 'username' not in request.POST:
        request.data.update({'username': request.data.get('email')})

    serialized = serializers.UserSerializer(data=request.data)

    if serialized.is_valid():
        user = User(**serialized.validated_data)
        user.save()

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)