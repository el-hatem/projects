from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from auctions.views import (
	IndexView, get_categories,
	CreateView, home,
	get_category, close_bid,
	ListingView, EditView,
	modify_watchlist, post_bid
)


app_name = 'auctions'

urlpatterns = [
	path("", home, name="home"),
	path("active-listings", IndexView.as_view(), name="index"),
	path("categories", get_categories, name="categories"),
	path("create", login_required(CreateView.as_view(), login_url="users:login"), name="create"),
	re_path("^edit/listing/(?P<id>[0-9]+)/$", login_required(EditView.as_view(), login_url="users:login"), name="edit"),
	path("category/<str:name>", get_category, name="category"),
	re_path("^listing/(?P<id>[0-9]+)/$", ListingView.as_view(), name="listing"),
	path("close/<int:list_id>", close_bid, name="close"),
	path("modify/<int:list_id>", modify_watchlist, name="modify_watchlist"),
	path("bid/<int:list_id>", post_bid, name="bid"),

]
