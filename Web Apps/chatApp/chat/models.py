from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_profile")
    image = models.ImageField(default="profile_pics/user-profile.png", upload_to='profile_pics', null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to="files/%Y/%m/%d", null=True, blank=True)

    def __str__(self):
        return self.message
