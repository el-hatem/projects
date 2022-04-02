from django.db import models


class ActiveListings(models.Model):
	title         = models.CharField(max_length=64, null=False, blank=False, unique=True)
	price         = models.DecimalField(max_digits=13, decimal_places=2, null=False, blank=False)
	description   = models.TextField(null=False, blank=False)
	state         = models.BooleanField(default=True)
	created_at    = models.DateTimeField(auto_now_add=True)
	image_url     = models.URLField(max_length=1024, unique=True, null=True, blank=True)
	category      = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='list', null=True, blank=True)
	user          = models.ForeignKey('users.User', related_name='created', on_delete=models.CASCADE, null=True, blank=True)


	class Meta:
		verbose_name = "activeListing"
		verbose_name_plural = "ActiveListings"

	def __str__(self):
		return self.title


class Category(models.Model):
	name  = models.CharField(max_length=64, null=False, blank=False, unique=True)


	class Meta:
		verbose_name = "category"
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name


class Bid(models.Model):
	nbids   = models.IntegerField(default=0)
	listing = models.OneToOneField('ActiveListings', on_delete=models.CASCADE, related_name='bid_item', null=False, blank=False)
	winner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bid_winner', null=True, blank=True)

	class Meta:
		verbose_name = "Bid"
		verbose_name_plural = "Bids"

	def __str__(self):
		return f'bid number: {self.id}'
