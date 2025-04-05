from chitchat.services.email_services.send_email_service import send_emails
from django.template.loader import render_to_string
from django.utils.timezone import now


def send_email_verification_link(user, activation_link):
    message = render_to_string(
        "chitchat/email_verification.html",
        {
            "user_name": user.username,
            "verification_link": activation_link,
            "current_year": now().year,
        },
    )
    return send_emails(
        recepient=user.email, subject="Verify Your Email", message=message
    )
