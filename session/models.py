from django.db import models
from user.models import User


class Session(models.Model):
    key = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    usage = models.TextField(default='Universal')
    finish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
