from django.db.models.signals import post_save
from django.dispatch import receiver
from chitchat.models import UserProfile, User
from django.core.cache import cache


def invalidate_cache_userdetails(user_id):
    cache_key = f"user_profile_{user_id}"
    cache.delete(cache_key)

# Invalidate cache when user model changes
@receiver(post_save, sender=User)
def invalidate_chathistory_user(sender, instance, **kwargs):
    invalidate_cache_userdetails(instance.id)

# Invalidate cache when userprofile model changes
@receiver(post_save, sender=UserProfile)
def invalidate_chathistory_userprofile(sender, instance, **kwargs):
    invalidate_cache_userdetails(instance.id)
