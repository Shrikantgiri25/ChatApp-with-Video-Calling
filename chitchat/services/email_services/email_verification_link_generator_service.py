from chitchat.services.email_services.email_verifying_token_generator_service import (
    generate_user_email_verification_token,
)
from chitchat.utils.helpers.constants import SOMETHING_WENT_WRONG


def generate_email_verification_link(user):
    try:
        token = generate_user_email_verification_token(user)
        activation_link = f"localhost:8000/activate/{token}/user/"
        return activation_link
    except Exception as e:
        raise Exception(SOMETHING_WENT_WRONG)
