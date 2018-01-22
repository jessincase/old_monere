from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from monere.feed.forms import NewPostForm
from monere.feed.models import Board, Post
from monere.chat.models import Room
from monere.chat.views import chat_room
from django.db import transaction
from django.shortcuts import render, redirect
from haikunator import Haikunator


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_posts(request, pk):
    board = get_object_or_404(Board, pk=pk)
    posts = Post.objects.filter(board=board).order_by('-date_published')
    return render(request, 'posts.html', {'board': board, 'posts': posts})

@login_required
def new_post(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.board = board
            post.original_poster = request.user

            new_room = None
            while not new_room:
                with transaction.atomic():
                    haikunator = Haikunator()
                    label = haikunator.haikunate()
                    if Room.objects.filter(label=label).exists():
                        continue
                    new_room = Room.objects.create(name=form.cleaned_data.get('title'),
                                                   poster=request.user,
                                                   label=label)
            post.room = new_room
            post.save()
            return redirect(chat_room, label=label)
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'board': board, 'form': form})
