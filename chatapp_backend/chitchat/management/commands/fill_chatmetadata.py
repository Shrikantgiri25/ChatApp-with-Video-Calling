from django.core.management.base import BaseCommand
from chitchat.models import Conversation, Message
from chitchat.models.user_conversation_metadata import UserConversationMetadata

class Command(BaseCommand):
    help = 'Populate UserConversationMetadata for existing conversations (private + group)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate UserConversationMetadata...')
        
        conversations = Conversation.objects.all()
        created_count, updated_count = 0, 0
        
        for conversation in conversations:
            self.stdout.write(f'Processing conversation: {conversation.id} ({conversation.conversation_type})')
            
            last_message = Message.objects.filter(conversation=conversation).order_by('-created_at').first()
            participants = []

            # 🔹 Handle private
            if conversation.conversation_type in ("private",):
                if conversation.user_one:
                    participants.append(conversation.user_one)
                if conversation.user_two:
                    participants.append(conversation.user_two)

            # 🔹 Handle groups (support both “group” and “groups”)
            elif conversation.conversation_type in ("group", "groups") and conversation.group:
                participants = list(conversation.group.members.all())
                if not participants:
                    self.stdout.write(f'  ⚠️ No members found for group {conversation.group.group_name}')
                    continue

            else:
                self.stdout.write(f'  ⚠️ Skipping conversation {conversation.id} — invalid type or missing group')
                continue

            # 🔹 Create or update metadata
            for user in participants:
                metadata, created = UserConversationMetadata.objects.get_or_create(
                    conversation=conversation,
                    user=user,
                    defaults={
                        'last_message_content': getattr(last_message, 'content', None),
                        'last_message_sender': getattr(last_message, 'sender', None),
                        'last_message_timestamp': getattr(last_message, 'created_at', None),
                        'unread_message_count': 0,
                    }
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1
                    if last_message:
                        metadata.last_message_content = last_message.content
                        metadata.last_message_sender = last_message.sender
                        metadata.last_message_timestamp = last_message.created_at
                        metadata.save()

                # 🔹 Update unread count
                unread_count = Message.objects.filter(
                    conversation=conversation, is_read=False
                ).exclude(sender=user).count()
                metadata.unread_message_count = unread_count
                metadata.save(update_fields=['unread_message_count'])

        self.stdout.write(
            self.style.SUCCESS(
                f'\nProcessed {conversations.count()} conversations — Created: {created_count}, Updated: {updated_count}'
            )
        )
