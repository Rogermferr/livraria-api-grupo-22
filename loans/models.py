from django.db import models


class Loan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField()
    status = models.BooleanField(default=False)
    
