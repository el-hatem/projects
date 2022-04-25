from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from orders.views import (
    OrdersView, OrderItemView, PaymentView,
    removeorder, reviewitem
)
app_name = 'orders'
# list of urls for dashborad
urlpatterns = [
    path('orders', login_required(OrdersView.as_view(), login_url='users:login'), name='orders'),
    path('pay', login_required(PaymentView.as_view(), login_url='users:login'), name='pay'),
    re_path('^order/(?P<id>[0-9]+)/$', login_required(OrderItemView.as_view(), login_url='users:login'), name='order'),
    re_path('^review/(?P<id>[0-9]+)/$', reviewitem, name='review'),
    re_path('^removeorder/(?P<id>[0-9]+)/$', removeorder, name='removeorder'),
]
