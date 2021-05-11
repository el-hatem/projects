from django.contrib import admin
from .models import (
	ActiveListings, Category, Bid
)

# Register your models here.
admin.site.register(ActiveListings)
admin.site.register(Category)
admin.site.register(Bid)
