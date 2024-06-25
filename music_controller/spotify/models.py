from django.db import models

from api.models import Room

# Create your models here.
class Spotify(models.Model):
    user = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=150)
    refresh_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    song = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


