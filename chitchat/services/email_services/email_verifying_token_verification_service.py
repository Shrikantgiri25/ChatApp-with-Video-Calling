from rest_framework_simplejwt.tokens import AccessToken
from chitchat.utils.helpers.constants import (
    USER_EMAIL_VERIFICATION,
    SOMETHING_WENT_WRONG,
    USER_NOT_EXISTS,
)
from chitchat.models.user_models import User
from rest_framework.exceptions import ValidationError


def verify_user_email_verification_token(token):
    try:
        token = AccessToken(token)
        user_id = token["user_id"]

        if token["purpose"] != USER_EMAIL_VERIFICATION:
            raise ValidationError("Invalid token purpose")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError(USER_NOT_EXISTS)

        if user.is_active == True:
            raise ValidationError("Link Expired. User already verified.")

        return user
    except ValidationError as e:
        raise e
    except Exception as e:
        raise Exception(SOMETHING_WENT_WRONG) from e
