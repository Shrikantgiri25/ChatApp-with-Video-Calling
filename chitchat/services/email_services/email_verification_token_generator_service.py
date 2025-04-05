from rest_framework_simplejwt.tokens import AccessToken
from chitchat.utils.helpers.constants import USER_EMAIL_VERIFICATION


def generate_user_email_verification_token(user):
    token = AccessToken()
    token["user_id"] = str(user.id)
    token["email"] = user.email
    token["purpose"] = USER_EMAIL_VERIFICATION
    return token
