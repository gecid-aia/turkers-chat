from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from users.models import User


class ChatManager(models.Manager):

    def get_collective_chat(self):
        return self.get(turker__isnull=True)

    def get_turker_chat(self, turker_id):
        return self.get(turker_id=turker_id)


class Chat(models.Model):
    objects = ChatManager()

    turker = models.OneToOneField(User, unique=True, null=True, on_delete=models.CASCADE)
    info = models.TextField(default='')

    def save(self, *args, **kwargs):
        if self.turker_id and not self.turker.is_turker:
            raise ValueError(f"User {self.turker} is not a turker.")
        elif not self.turker_id:
            try:
                chat = Chat.objects.get_collective_chat()
                raise ValueError(f"Collective chat already exists with the id {chat.id}")
            except Chat.DoesNotExist:
                pass
        return super().save(*args, **kwargs)

    @property
    def is_collective(self):
        return not self.turker_id

    @property
    def title(self):
        return "Collective Chat" if self.is_collective else self.turker.username

    @property
    def messages_url(self):
        return reverse('chats_api:chat_messages', args=[self.id])

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    @property
    def sender_username(self):
        if not self.sender:
            return 'Anonymous'
        return self.sender.username

    @property
    def turker_chat_url(self):
        if not self.sender or self.sender.is_regular:
            return ''
        return reverse('chats_api:chat', args=[self.sender.chat.id])


@receiver(post_save, sender=User)
def create_turker_chat(sender, instance, created, *args, **kwargs):
    if created and instance.is_turker:
        Chat.objects.create(turker=instance)
