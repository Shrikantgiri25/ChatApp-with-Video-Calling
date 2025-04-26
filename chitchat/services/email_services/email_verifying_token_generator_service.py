from rest_framework_simplejwt.tokens import AccessToken
from chitchat.utils.helpers.constants import (
    USER_EMAIL_VERIFICATION,
    SOMETHING_WENT_WRONG,
)


def generate_user_email_verification_token(user):
    try:
        token = AccessToken()
        token["user_id"] = str(user.id)
        token["email"] = user.email
        token["purpose"] = USER_EMAIL_VERIFICATION
        return token
    except Exception as e:
        raise Exception(SOMETHING_WENT_WRONG)
