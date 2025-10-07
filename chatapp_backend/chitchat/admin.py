from django.contrib import admin
from .models import (
    Attachment,
    Call,
    Conversation,
    Group,
    Message,
    Notification,
    User,
    UserProfile,
    IssuedToken,
    UserConversationMetadata
)


# Register your models here.
admin.site.register(Attachment)
admin.site.register(Call)
admin.site.register(Conversation)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(IssuedToken)
admin.site.register(UserConversationMetadata)
admin.site.site_header = "ChitChat Admin"
