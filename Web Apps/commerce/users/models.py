from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
	won_list        = models.ManyToManyField('auctions.ActiveListings', related_name='won', null=True, blank=True)
	watched_list    = models.ManyToManyField('auctions.ActiveListings', related_name='watched', null=True, blank=True)


	class Meta:
		verbose_name = "user"
		verbose_name_plural = "Users"

	def __str__(self):
		return self.username


class Comments(models.Model):
	description  = models.TextField(null=False, blank=False)
	created_at   = models.DateTimeField(auto_now_add=True)
	user         = models.ForeignKey('User', related_name='comment', null=True, blank=True, on_delete=models.CASCADE, unique=False)
	listing      = models.ForeignKey('auctions.ActiveListings', on_delete=models.CASCADE, related_name='comment', null=True, blank=True, unique=False)


	class Meta:
		verbose_name = "comment"
		verbose_name_plural = "Comments"

	def __str__(self):
		return self.description

