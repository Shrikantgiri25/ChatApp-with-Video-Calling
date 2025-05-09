from chitchat.services.email_services.send_email_service import send_emails
from django.template.loader import render_to_string
from django.utils.timezone import now
from chitchat.utils.helpers.constants import SOMETHING_WENT_WRONG


def send_email_verification_link(user, activation_link):
    try:
        message = render_to_string(
            "chitchat/email_verification.html",
            {
                "email": user.email,
                "verification_link": activation_link,
                "current_year": now().year,
            },
        )
        return send_emails(
            recepient=user.email, subject="Verify Your Email", message=message
        )
    except Exception as e:
        raise Exception(SOMETHING_WENT_WRONG)
