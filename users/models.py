from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=127, unique=True)
    password = models.CharField(max_length=20)
    full_name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    block_date = models.DateField(null=True)
    user_loan = models.ManyToManyField('copies.Copy', through='loans.Loan', related_name='copies_loans_user')