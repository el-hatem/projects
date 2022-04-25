from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from dashboard.views import (
    Homepage, ItemView,
    Menu, About, CartView, WatchlistView, OrdertableView, paymentdetails
)

app_name = 'dashboard'
# list of urls for dashborad
urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path('menu', Menu.as_view(), name='menu'),
    path('about', About.as_view(), name='about'),
    path('cart', login_required(CartView.as_view(), login_url='users:login'), name='cart'),
    path('watchlist', login_required(WatchlistView.as_view(), login_url='users:login'), name='watchlist'),
    path('ordertable', login_required(OrdertableView.as_view(), login_url='users:login'), name='ordertable'),
    re_path('^item/(?P<id>[0-9]+)/$', login_required(ItemView.as_view(), login_url='users:login'), name='item'),
    re_path('^paymentdetails/(?P<id>[0-9]+)/$', paymentdetails, name='paymentdetails'),
]
