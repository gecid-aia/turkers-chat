from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser


class USER_TYPE(Enum):
    RG = 'RG'
    TK = 'TK'

class User(AbstractUser):
    user_type = models.CharField(max_length=2, choices=USER_TYPE, blank=False, null=False, default=USER_TYPE.RG)

    @property
    def is_regular(self):
        return self.user_type == USER_TYPE.RG

    @property
    def is_turker(self):
        return self.user_type == USER_TYPE.TK
