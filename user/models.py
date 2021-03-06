from django.db import models


class User(models.Model):
    username = models.TextField(unique=True)
    public_key = models.TextField(unique=True)
    signature = models.TextField()
    is_admin = models.BooleanField(default=False)
