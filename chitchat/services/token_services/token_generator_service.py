from rest_framework_simplejwt.tokens import AccessToken
from chitchat.utils.helpers.constants import (
    SOMETHING_WENT_WRONG,
)
from datetime import timedelta, datetime
from django.utils import timezone
from chitchat.models.issued_tokens import IssuedToken


def generate_token(user, purpose, lifetime=5):  # lifetime in minutes
    try:
        is_issued_token = IssuedToken.objects.filter(
            user=user,
            purpose=purpose,
            is_active=True,
        ).first()

        if is_issued_token and not is_issued_token.is_expired():
            return is_issued_token
        elif is_issued_token:
            is_issued_token.is_active = False
            is_issued_token.save()

        token = AccessToken()
        token["email"] = user.email
        token["purpose"] = purpose
        token.set_exp(
            from_time=datetime.now(timezone.utc), lifetime=timedelta(minutes=lifetime)
        )

        token_str = str(token)
        is_issued_token = IssuedToken.objects.create(
            user=user,
            token=token_str,
            purpose=purpose,
            expires_at=timezone.now() + timedelta(minutes=lifetime),
        )
        return is_issued_token

    except Exception as e:
        import traceback

        print("Error during token generation:", e)
        traceback.print_exc()
        raise Exception(SOMETHING_WENT_WRONG)
