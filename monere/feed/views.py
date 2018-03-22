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
from django.views.generic import CreateView, UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator



def home(request):
    boards = Board.objects.all()
    if request.user.is_authenticated():
        rooms = Room.objects.filter(poster=request.user)
        return render(request, 'home.html', {'boards': boards, 'rooms': rooms})

    return render(request, 'home.html', {'boards': boards})

def board_posts(request, pk):
    board = get_object_or_404(Board, pk=pk)
    posts = Post.objects.filter(board=board).order_by('-date_published')
    if request.user.is_authenticated():
        rooms = Room.objects.filter(poster=request.user)
        return render(request, 'posts.html', {'board': board, 'posts': posts, 'rooms': rooms})
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

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'description',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(original_poster=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('board_posts', pk=post.board.pk)