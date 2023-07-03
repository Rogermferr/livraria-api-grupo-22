from django.db import models

class Loan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    return_date = models.DateField()
    is_finished = models.BooleanField(default=False)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT)
    copy = models.ForeignKey('copies.Copy', on_delete=models.PROTECT)
