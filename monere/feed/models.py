from django.db import models
from django.conf import settings
from monere.chat.models import Room
from datetime import datetime

class Board(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_posts_count(self):
        return Post.objects.filter(board=self).count()

    def get_last_post(self):
        return Post.objects.filter(board=self).order_by('-date_published').first()


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_published = models.DateTimeField(default=datetime.now, editable=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='category')
    original_poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='original_poster')
    room = models.OneToOneField(Room, to_field='room_id',primary_key=True, on_delete=models.CASCADE, related_name='room')

    def __str__(self):
        return self.title

