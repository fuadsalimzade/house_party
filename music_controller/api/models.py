from django.db import models
import secrets

def generate_unique_code():
    code = secrets.token_hex(3).upper()
    return code

# Create your models here.
class Room(models.Model):
    code = models.CharField(unique=True, max_length=8, default=generate_unique_code)
    host = models.CharField(unique=True, max_length=50)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50, null=True)
