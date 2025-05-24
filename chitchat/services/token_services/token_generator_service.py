from rest_framework_simplejwt.tokens import AccessToken
from chitchat.utils.helpers.constants import (
    SOMETHING_WENT_WRONG,
)
from datetime import timedelta, datetime, timezone
from chitchat.models.issued_tokens import IssuedToken
from django.utils import timezone as issue_time


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
            expires_at=issue_time.now() + timedelta(minutes=lifetime),
        )
        return is_issued_token

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise Exception(SOMETHING_WENT_WRONG)
