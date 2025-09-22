from chitchat.services.token_services.token_generator_service import (
    generate_token,
)
from chitchat.utils.helpers.constants import (
    SOMETHING_WENT_WRONG,
    USER_EMAIL_VERIFICATION,
)


def generate_email_verification_link(user):
    try:
        token = generate_token(
            user=user, purpose=USER_EMAIL_VERIFICATION, lifetime=60 * 24 * 3
        )  # 3 days
        activation_link = f"localhost:8000/api/v1/verify/{token.id}/email/"
        return activation_link
    except Exception as e:
        raise Exception(SOMETHING_WENT_WRONG)
