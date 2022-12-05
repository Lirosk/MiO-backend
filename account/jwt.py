from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")

        if len(auth_token) != 2:
            raise AuthenticationFailed('Token is invalid')

        token = auth_token[1]

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            email = payload['email']
            user = User.objects.get(email=email)

            return (user, token)

        except jwt.ExpiredSignatureError as ex:
            raise AuthenticationFailed('Token is expired.')
        except jwt.DecodeError as ex:
            raise AuthenticationFailed('Token is invalid.')
        except User.DoesNotExist as no_user:
            raise AuthenticationFailed('No such user')
