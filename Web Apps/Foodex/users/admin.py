from django.contrib import admin
from users.models import (
    User, Cart, Card, Rating
)
# Register your models here.
admin.site.register(Cart)
admin.site.register(User)
admin.site.register(Card)
admin.site.register(Rating)
