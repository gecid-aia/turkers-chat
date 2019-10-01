from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    RG = 'RG'
    TK = 'TK'

    USER_TYPE = [
        (RG, 'Regular User'),
        (TK, 'Turker User'),
    ]

    user_type = models.CharField(max_length=2, choices=USER_TYPE, blank=False, null=False, default=RG)