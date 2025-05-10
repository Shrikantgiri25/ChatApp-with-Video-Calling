# yourapp/signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def maybe_activate_google_user(request, user, **kwargs):
    print("Google login signal triggered")
    sociallogin = kwargs.get('sociallogin')
    if sociallogin and sociallogin.account.provider == 'google':
        extra_data = sociallogin.account.extra_data
        if extra_data.get('email_verified'):
            user.status = 'NEW_USER'
            user.is_active = True
            user.save()
