from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Generate JWT access and refresh tokens for a user.
    """

    if not user.is_active:
        raise ValueError("Inactive users cannot receive tokens.")

    refresh = RefreshToken.for_user(user)

    # Keep custom JWT claims minimal.
    refresh["email"] = user.email

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_user_response(user):
    """
    Return the standard user representation
    used in authentication responses.
    """

    return {
        "id": str(user.pk),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_email_verified": user.is_email_verified,
    }