from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.TextField()
    poster = models.ForeignKey(User, related_name='poster')
    room_id = models.AutoField(primary_key=True)
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    user = models.ForeignKey(User, related_name='user')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    #@login_required
    #def get_user(self):

    def __unicode__(self):
        return '[{timestamp}] {user}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return {'user': self.user, 'message': self.message, 'timestamp': self.formatted_timestamp}