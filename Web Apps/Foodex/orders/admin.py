from django.contrib import admin
from orders.models import (
    Order, Item, Payment, Tables
)
# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Tables)
