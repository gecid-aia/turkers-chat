from django.db import models

from users.models import User


class Chat(models.Model):
    turker = models.ForeignKey(User, unique=True, null=True, on_delete=models.PROTECT)
    info = models.TextField(default='')
