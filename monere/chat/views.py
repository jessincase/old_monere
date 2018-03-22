import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from django.template.loader import render_to_string
from django.http import JsonResponse
import haikunator
from .models import Room
from monere.feed.models import Post


def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)

@login_required
def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    room = get_object_or_404(Room,label=label)
    post = get_object_or_404(Post,room=room )
    messages = reversed(room.messages.order_by('-timestamp'))

    return render(request, "room.html", {
        'room': room,
        'messages': messages,
        'post': post,
    })


@login_required
def popup_chatroom(request, label):
    room = get_object_or_404(Room, label=label)
    #post = get_object_or_404(Post, room=room)
    messages = reversed(room.messages.order_by('-timestamp'))
    user = request.user

    room_html = render_to_string('popup_chatroom.html', {'room': room, 'messages': messages, 'user': user})
    output_data = {'room_html': room_html}
    return JsonResponse(output_data)
    #return render(request, 'popup_chatroom.html', {'room': room, 'messages': messages})

@login_required
def user_rooms_sidebar(request):
    rooms = Room.objects.filter(poster=request.user)
    room_count = len(rooms)

    return render(request, "sidebar.html", {'rooms': rooms, 'room_count': room_count})

def save_room(request, label):
    room = get_object_or_404(Room, label=label)
    user = request.user
    user.saved_rooms.add(room)
    user.save()

    #render HttpRe
