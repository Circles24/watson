from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    level = models.IntegerField()
    status_choices = (('p', 'pending'), ('i', 'initiated'), ('c', 'completed'))
    status = models.CharField(default='p', max_length=1, choices=status_choices)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True)
    freq_data = models.JSONField(default=dict)

class Page(models.Model):
    url = models.CharField(max_length=200)
    text = models.TextField()
    last_updated_at = models.DateTimeField()
    urls = models.JSONField(default=list)
