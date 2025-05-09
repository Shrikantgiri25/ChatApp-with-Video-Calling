from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def maybe_activate_google_user(request, user, **kwargs):
    sociallogin = kwargs.get('sociallogin')
    if sociallogin and sociallogin.account.provider == 'google':
        extra_data = sociallogin.account.extra_data
        if extra_data.get('email_verified'):
            user.is_email_verified = True
            user.save()
