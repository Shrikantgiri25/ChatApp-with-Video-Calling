from chitchat.services.email_services.email_verification_token_generator_service import (
    generate_user_email_verification_token,
)


def generate_email_verification_link(user):
    token = generate_user_email_verification_token(user)
    activation_link = f"localhost:8000/activate/{token}/user/"
    return activation_link
