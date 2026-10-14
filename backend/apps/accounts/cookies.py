from django.conf import settings
from rest_framework_simplejwt.settings import api_settings

def set_refresh_cookie(response, refresh):
    response.set_cookie(
        settings.AUTH_REFRESH_COOKIE_NAME, refresh,
        max_age=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
        httponly=True, secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path=settings.AUTH_REFRESH_COOKIE_PATH,
    )

def clear_refresh_cookie(response):
    response.delete_cookie(
        settings.AUTH_REFRESH_COOKIE_NAME,
        path=settings.AUTH_REFRESH_COOKIE_PATH,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )
    response.cookies[settings.AUTH_REFRESH_COOKIE_NAME]["httponly"] = True
    response.cookies[settings.AUTH_REFRESH_COOKIE_NAME]["secure"] = settings.AUTH_COOKIE_SECURE