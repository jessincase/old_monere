"""monere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from monere.accounts import views as accounts_views
from monere.feed import views
from monere.chat import views as chat_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^sidebar/$', chat_views.user_rooms_sidebar, name='sidebar'),
    url(r'^popup_chatroom/(?P<label>[\w-]{,50})/$', chat_views.popup_chatroom, name='popup_chatroom'),
    url(r'^(?P<label>[\w-]{,50})/$', chat_views.chat_room, name='chat_room')
]


