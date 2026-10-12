from django.utils.translation import gettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction

from rest_framework import serializers
from rest_framework.serializers import ValidationError as DRFValidatorError

from rest_framework.exceptions import AuthenticationFailed

from .models import Profile

from .authentication import user_can_authenticate

from .services import (
    get_tokens_for_user,
    get_user_response,
)

User = get_user_model()


def password_field(**kwargs):
    # optional: for setdefault to show error messages
    kwargs.setdefault("error_messages", {
        "blank": _("Password is required."),
        "null": _("Password is required."),
    })
    return serializers.CharField(
        write_only=True, trim_whitespace=False, max_length=128,
        style={"input_type": "password"}, **kwargs,
    )

class UserSerializer(serializers.ModelSerializer):
    """
    Current user representation.
    """
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_email_verified", "date_joined")

        read_only_fields = ("id", "email", "is_email_verified", "date_joined")


class RegisterSerializer(serializers.Serializer):
    """
    register new user
    """
    email = serializers.EmailField(max_length=254)
    password = password_field()
    password_confirm = password_field()
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate_email(self, value):
        value = User.objects.normalize_email(value)
        if User.objects.filter(email__iexact=value).exists():
            raise DRFValidatorError (
                _("Registration with this email is not possible")
            )
        return value
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise DRFValidatorError(
                {"password_confirm": _("The repeated password does not match")}
            )
        candidate = User(**{key: value for key, value in attrs.items()
                            if key not in {"password", "password_confirm"}})
        try:
            validate_password(attrs["password"], user=candidate)
        
        except DjangoValidationError as exc:
            raise DRFValidatorError({"password": list(exc.messages)}) from exc
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        email=validated_data["email"]
        try:
            with transaction.atomic():
                return User.objects.create_user(**validated_data)
        except IntegrityError as exc:
            raise DRFValidatorError(
                {"email": _("Registration with this email is not possible")}
            ) from exc


class LoginSerializer(serializers.Serializer):
    """
    Login using email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=User.objects.normalize_email(attrs["email"]),
            password=attrs["password"],
        )

        if user is None:
            raise AuthenticationFailed(
                {
                    "detail": _("Email or password is incorrect")
                }
            )
        if not user_can_authenticate(user):
            raise AuthenticationFailed(
                {
                    "detail": _("First, verify your email")
                }
            )
        
        return {"user": user}

        # tokens = get_tokens_for_user(user)

        # return {
        #     **tokens,
        #     "user": get_user_response(user),
        # }


class ProfileSerializer(serializers.ModelSerializer):
    """
    User profile representation.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id"
            "user",
            "avatar",
            "bio",
            "default_page_size",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Update profile and basic user information.
    """
    first_name = serializers.CharField(
        source="user.first_name",
        max_length=150,
        required=False,
        allow_blank=True,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        max_length=150,
        required=False,
        allow_blank=True,
    )

    bio = serializers.CharField(
        max_length=2000,
        required=False,
        allow_blank=True,
    )
    
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "bio",
            "default_page_size",
            "first_name",
            "last_name",
        )
    
    def validate_avatar(self, value):
        try:
            return norma

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        if user_data:
            # QuerySet.update avoids overwriting unrelated User fields
            user = instance.user

            for attr, value in user_data.items():
                setattr(user, attr, value)

            user.save(
                update_fields=list(user_data.keys())
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance