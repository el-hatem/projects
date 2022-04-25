from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from users.views import (
    Login, Register, logout_view,
    Settings, removewatchlist, addwatchlist,
    add_card, delete_card
)
app_name = 'users'
# list of urls for user app
urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('me', login_required(Settings.as_view(), login_url='users:login'), name='profile'),
    re_path('^addwatchlist/(?P<id>[0-9]+)/$', addwatchlist, name='addwatchlist'),
    re_path('^removewatchlist/(?P<id>[0-9]+)/$', removewatchlist, name='removewatchlist'),
    path('addcard', add_card, name='addcard'),
    path('deletecard', delete_card, name='deletecard'),
    path('logout', logout_view, name='logout')
]
