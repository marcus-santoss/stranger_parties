from django.contrib.auth.models import AbstractUser
from django.db import models

from stranger_parties.core.managers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["id", "created_at", "updated_at"]
        abstract = True


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(null=False, blank=False, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()
