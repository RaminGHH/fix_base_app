from django.conf import settings

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


def user_can_authenticate(user):
    return bool(
        user and user.is_active
        and user.is_email_verified
    )

class AccountJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        if not user_can_authenticate(user):
            raise AuthenticationFailed('ورود به این حساب مجار نیست')
        return user