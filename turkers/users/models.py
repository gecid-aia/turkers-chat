from enum import Enum
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def turkers(self):
        return self.get_queryset().filter(user_type=USER_TYPE.Turker.value)


class USER_TYPE(Enum):
    Regular = "RG"
    Turker = "TK"


class User(AbstractUser):
    objects = UserManager()

    user_type = models.CharField(
        max_length=2,
        choices=[(t.value, t.name) for t in USER_TYPE],
        blank=False,
        null=False,
        default=USER_TYPE.Regular.value,
    )
    uuid = models.UUIDField(db_index=True, null=True, editable=False)

    @property
    def is_regular(self):
        return self.user_type == USER_TYPE.Regular.value

    @property
    def is_turker(self):
        return self.user_type == USER_TYPE.Turker.value

    def save(self, *args, **kwargs):
        if self.is_turker and not self.uuid:
            self.uuid = uuid4()
        return super().save(*args, **kwargs)
