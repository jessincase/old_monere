from django.db import models
from django.contrib.auth.models import AbstractUser
from monere.chat.models import Room

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    saved_rooms = models.ManyToManyField(Room)