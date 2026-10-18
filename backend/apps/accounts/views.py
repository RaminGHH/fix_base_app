from django.conf import settings
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token, rotate_token
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings

from .cookies import clear_refresh_cookie, set_refresh_cookie
from .models import Profile
from .permissions import CsrfRequired

from .serializers import (
    EmailRequestSerializer, LinkConfirmSerializer, LoginSerializer,
    PasswordChangeSerializer, PasswordResetConfirmSerializer,
    ProfileSerializer, ProfileUpdateSerializer, RegisterSerializer, UserSerializer,
)
from .services import (
    change_password, confirm_email, confirm_password_reset, get_tokens_for_user,
    revoke_refresh, rotate_refresh, send_account_email, send_email_after_commit,
)

User = get_user_model()