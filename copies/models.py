from django.db import models


class Copy(models.Model):
    number_copies = models.IntegerField()
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
