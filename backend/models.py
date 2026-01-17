from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True, default=None)
    color = models.CharField(max_length=7, null=True, default=None)
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)


class Entry(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, default=None)
