from django.apps import AppConfig


class ChitchatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chitchat"

    def ready(self):

        # Google login signal
        # This will import the signal handlers when the app is ready    
        import chitchat.signals.google_login