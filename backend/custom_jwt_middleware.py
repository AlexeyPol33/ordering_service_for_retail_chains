import jwt
from django.conf import settings
from app.models import User


class CustomJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)

        if token:
            try:
                token = token.split(' ')[1]
                decoded_payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )
                user_id = decoded_payload['user_id']
                user = User.objects.get(pk=user_id)
                request.user = user
            except jwt.ExpiredSignatureError:
                request.auth_failed = 'Token has expired'
            except jwt.DecodeError:
                request.auth_failed = 'Token is invalid'
            except User.DoesNotExist:
                request.auth_failed = 'No such user'
            except Exception as e:
                request.auth_failed = f'invalid authorization format: {e}'

        response = self.get_response(request)
        return response
