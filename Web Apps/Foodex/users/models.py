from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from orders.models import (
    Item
)
# Create your models here.


# create User model
class User(AbstractUser):
    # relations
    favourites    = models.ManyToManyField('orders.Item', related_name='favourite', null=True, blank=True)
    cart          = models.OneToOneField('users.Cart', on_delete=models.CASCADE, related_name='usercart', null=True, blank=True, db_constraint=False)
    card          = models.OneToOneField('users.Card', on_delete=models.DO_NOTHING, related_name='card', null=True, blank=True, db_constraint=False)
    # premative fields
    location      =  models.CharField(max_length=250, null=False, blank=False)
    phone         =  models.CharField(max_length=11, null=False, blank=False, unique=True)


    class Meta:
        verbose_name = "user"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Card(models.Model):
    cardowner             = models.CharField(max_length=25, null=False, blank=False, default='admin')
    cardnumber            = models.IntegerField(unique=True, null=False, blank=False)
    cvv                   = models.IntegerField(null=False, blank=False, validators=[MaxValueValidator(999), MinValueValidator(100)])
    expired_date          = models.DateField()
    budget                = models.DecimalField(default=320.50, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "card"
        verbose_name_plural = "Cards"

    def __str__(self):
        return f'{self.cardnumber}'


class Cart(models.Model):

    state_choices = [
        (0, 'Deactived'),
        (1, 'actived')
    ]

    # relations
    # premative fields
    state       = models.BooleanField(default=0, choices=state_choices)
    totalprice  = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = "cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart id: {self.id} Cart now is: {self.state}"


class Rating(models.Model):
    # relations
    user         = models.ForeignKey('users.User', related_name='comment', null=True, blank=True, on_delete=models.CASCADE, unique=False)
    item         = models.ForeignKey('orders.Item', on_delete=models.CASCADE, related_name='rating', null=True, blank=True, unique=False)
    # premitive attrs
    rate         = models.IntegerField()
    description  = models.TextField(null=False, blank=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "rate"
        verbose_name_plural = "Rates"

    def __str__(self):
        return f"{self.user.username} has rated {self.item.title} with {self.rate} starts"



