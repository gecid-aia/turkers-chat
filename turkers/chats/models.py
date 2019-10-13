from django.db import models

from users.models import User


class Chat(models.Model):
    turker = models.OneToOneField(User, unique=True, null=True, on_delete=models.PROTECT)
    info = models.TextField(default='')

    def save(self, *args, **kwargs):
        if self.turker_id and not self.turker.is_turker:
            raise ValueError(f"User {self.turker} is not a turker.")
        elif not self.turker_id:
            if Chat.objects.filter(turker__isnull=True).exists():
                raise ValueError(f"System can have only one general chat")
        return super().save(*args, **kwargs)

    @property
    def title(self):
        if not self.turker_id:
            return "Colective Chat"
        return self.turker.username
