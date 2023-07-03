from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=127)
    author = models.CharField(max_length=127)
    pages = models.IntegerField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_copies = models.IntegerField()
    user = models.ManyToManyField("users.User", related_name="user_books")
