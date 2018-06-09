from django.db import models
from user.models import User


class Message(models.Model):
    sender = models.ForeignKey(to=User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(to=User, related_name='receiver', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
