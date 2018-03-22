from __future__ import unicode_literals
from channels import Group
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.conf import settings


class Room(models.Model):
    name = models.TextField()
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='poster')
    room_id = models.AutoField(primary_key=True)
    label = models.SlugField(unique=True)
    users_in_chat = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now,db_index=True)


    def __unicode__(self):
        return '[{timestamp}] {user}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
        #.strptime(self.timestamp, format)
    
    def as_dict(self):
        return {'user': self.user, 'message': self.message, 'timestamp': self.formatted_timestamp}
