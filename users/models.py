from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=127, unique=True)
    password = models.CharField(max_length=20)
    available_loan = models.BooleanField(default=True, read_only=True)