from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status, views
from rest_framework.request import Request
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import models
from . import emails, serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponseRedirect


User = get_user_model()


class UserRegisterAPIView(CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        after_email_verification = serializer.validated_data['redirect_to']
        redirect = models.Redirect(user=user, after_email_verification=after_email_verification)
        redirect.save()

        emails.send_account_verification_email(
            user, request, 'account/verify-email/')
        return Response({'message': 'User has been registered, check email for verification.', **serializer.data}, status=status.HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerificationAPIView(GenericAPIView):
    serializer_class = serializers.EmailVerificationSerializer
    permission_classes = (AllowAny, )
    authentication_classes = []

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        serialized = self.serializer_class(request.GET)

        token = serialized.data.get('token')
        email = serialized.data.get('email')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(email=payload['email'])
            if not user.email_verified:
                user.email_verified = True
                user.save()

            redirect = models.Redirect.objects.get(user=user)
            return HttpResponseRedirect(f"{redirect.after_email_verification}?token={user.token}")
        except jwt.exceptions.ExpiredSignatureError as e:
            try:
                user = User.objects.get(email=email)
                emails.end_account_verification_email(user, request, "account/verify-email/")
            except User.DoesNotExist: ...
            return Response({'message': "Verify email token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'message': 'Verify email token is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"message": 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            emails.send_password_reset_email(user, uidb64, token)
        except User.DoesNotExist as e:
            return Response({'message': 'User with such email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Link has been sent to your mail.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message': "Password reset credentials are valid.",
                    "uidb64": uidb64,
                    "token": token
                },
                    status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as e:
            ...

        return Response({'message': 'Password reset credentials are invalid.'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = serializers.SetNewPasswordSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password reset success'}, status=status.HTTP_200_OK)


class PasswordResetInPlaceAPIView(GenericAPIView):
    serializer_class = serializers.PasswordResetInPlaceSerializer

    password = openapi.Parameter("password", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)
    new_password = openapi.Parameter("new_password", in_=openapi.IN_BODY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "password": password,
            "new_password": new_password
        }
    ))
    def post(self, request):
        user = request.user
        request.data["email"] = user.email
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        user.set_password(serialized.validated_data["new_password"])
        user.save()

        return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)