from django.db import models

# Create your models here.

class Numbers(models.Model):
    value=models.IntegerField(unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
