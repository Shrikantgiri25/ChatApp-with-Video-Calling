from rest_framework_simplejwt.tokens import AccessToken
from chitchat.utils.helpers.constants import (
    SOMETHING_WENT_WRONG,
)

from rest_framework.exceptions import ValidationError
from chitchat.models.issued_tokens import IssuedToken

def verify_decode_token(token, purpose):
    try:
        token = AccessToken(token)
        if token["purpose"] != purpose:
            raise ValidationError("Invalid token purpose")
        try:
            issued_token = IssuedToken.objects.get(
                token=str(token),
                purpose=purpose,
                is_active=True,
            )
            if issued_token.is_expired():
                raise ValidationError("Token has expired")
            issued_token.is_active = False
            issued_token.save()
        except IssuedToken.DoesNotExist:
            raise ValidationError("Token does not exist or is inactive")
        return token
    except ValidationError as e:
        raise e
    except Exception as e:
        raise Exception(SOMETHING_WENT_WRONG) from e
