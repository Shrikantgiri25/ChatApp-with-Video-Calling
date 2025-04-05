from django.core.mail import send_mail
from django.core.mail import BadHeaderError
import smtplib
from chitchat.utils.env_config import EnviromentConfigs as env


class EmailVerificationError(Exception):
    pass


def send_emails(recepient, subject, message):
    if not recepient:
        raise EmailVerificationError("Recipient Email is missing")
    if not subject:
        raise EmailVerificationError("Email Subject is missing")
    if not message:
        raise EmailVerificationError("Email Message is missing")
    try:
        plain_message = (
            f"Hi {recepient},\nThank you for joining us, let make world a better place."
        )
        send_mail(
            subject=subject,
            html_message=message,
            message=plain_message,
            from_email="shrikantgiri218@gmail.com",
            fail_silently=False,
            recipient_list=[recepient],
        )
    except smtplib.SMTPAuthenticationError as e:
        raise EmailVerificationError(f"SMTP Error occurred: {str(e)}")
    except smtplib.SMTPException as e:
        raise EmailVerificationError(f"SMTP Error occurred: {str(e)}")
    except BadHeaderError as e:
        raise EmailVerificationError(f"Invalid header found: {str(e)}")
    except Exception as e:
        raise EmailVerificationError(
            f"Unexpected error occured while sending email: {str(e)}"
        )
