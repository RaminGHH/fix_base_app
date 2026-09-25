from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from django.db import transaction

from rest_framework import serializers

from .models import Profile
from .services import (
    get_tokens_for_user,
    get_user_response,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Current user representation.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_email_verified",
            "date_joined",
        )

        read_only_fields = (
            "id",
            "email",
            "is_email_verified",
            "date_joined",
        )


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
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                {
                    "detail": "ایمیل یا رمز عبور صحیح نیست."
                }
            )

        tokens = get_tokens_for_user(user)

        return {
            **tokens,
            "user": get_user_response(user),
        }


class ProfileSerializer(serializers.ModelSerializer):
    """
    User profile representation.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "user",
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Update profile and basic user information.
    """

    first_name = serializers.CharField(
        source="user.first_name",
        required=False,
        allow_blank=True,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = Profile
        fields = (
            "avatar",
            "bio",
            "first_name",
            "last_name",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        if user_data:
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