from django.contrib import admin
from .models import (
	User, Comments
)

# Register your models here.
admin.site.register(User)
admin.site.register(Comments)