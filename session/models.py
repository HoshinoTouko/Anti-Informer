from django.db import models


class Session(models.Model):
    key = models.TextField()
    usage = models.TextField()
    finish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
