from django.urls import path
from django.contrib.auth.decorators import login_required
from users.views import (
	LoginView,
	RegisterView,
	logout_view,
	EditSittingsView,
	owned_list, watch_list
)


app_name = 'users'

urlpatterns = [
	path("login", LoginView.as_view(), name="login"),
	path("logout", logout_view, name="logout"),
	path("register", RegisterView.as_view(), name="register"),
	path("settings", login_required(EditSittingsView.as_view(), login_url="users:login"), name="settings"),
	path("lists/me", owned_list, name="mylists"),
	path("watch-lists/me", watch_list, name="watchlist"),
]
