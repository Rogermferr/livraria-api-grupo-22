from django.db import models


class Copy(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
