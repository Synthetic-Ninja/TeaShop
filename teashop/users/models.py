from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True)
    image = models.ImageField(upload_to='users_image', null=True, blank=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    is_verified_email = models.BooleanField(default=False)

