from rest_framework_simplejwt.tokens import AccessToken
from chitchat.utils.helpers.constants import SOMETHING_WENT_WRONG
from rest_framework.exceptions import ValidationError
from chitchat.models.issued_tokens import IssuedToken

def verify_decode_token(token_id, purpose):
    try:
        # Retrieve the issued token from the database
        issued_token = IssuedToken.objects.get(
            id=token_id,
            purpose=purpose,
            is_active=True,
        )
        token_str = issued_token.token

        # Decode the token from the JWT string
        token = AccessToken(token_str)
        # Check the token's purpose and expiration
        if token["purpose"] != purpose:
            raise ValidationError("Invalid token purpose")
        if issued_token.is_expired():
            raise ValidationError("Token has expired")

        # Deactivate the token
        issued_token.is_active = False
        issued_token.save()

        return token

    except IssuedToken.DoesNotExist:
        raise ValidationError("Token does not exist or is inactive")
    except ValidationError as e:
        raise e
    except Exception as e:
        raise Exception(SOMETHING_WENT_WRONG) from e
