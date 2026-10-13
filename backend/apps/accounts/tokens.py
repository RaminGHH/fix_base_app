from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Different salt prevents password-reset and verification token substitution.
    """
    key_salt = "fixbase.accounts.email-verification"

    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.password}{timestamp}{user.email}{user.is_email_verified}'

email_verification_token = EmailVerificationTokenGenerator()