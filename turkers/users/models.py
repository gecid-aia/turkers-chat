from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser


class USER_TYPE(Enum):
    Regular = 'RG'
    Turker = 'TK'

class User(AbstractUser):
    user_type = models.CharField(max_length=2, choices=[(t.value, t.name) for t in USER_TYPE], blank=False, null=False, default=USER_TYPE.Regular.value)

    @property
    def is_regular(self):
        return self.user_type == USER_TYPE.Regular.value

    @property
    def is_turker(self):
        return self.user_type == USER_TYPE.Turker.value
