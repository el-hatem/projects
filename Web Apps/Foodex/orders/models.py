from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Item(models.Model):


    # global variables
    type_options = [
        ('new', 'new'),
        ('sale', 'sale'),
        ('defualt', 'defualt'),
        ('out of stock', 'out of stock')
    ]
    cat_options = [
        ('pizza', 'pizza'),
        ('pasta', 'pasta'),
        ('burger', 'burger'),
        ('drinks', 'drinks'),
        ('salads', 'salads'),
        ('dessert', 'dessert')]
    # relations attr

    # premitive attrs
    img           = models.URLField(max_length=1024, unique=True, null=True, blank=True)
    title         = models.CharField(max_length=64, null=False, blank=False, unique=True)
    price         = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    description   = models.TextField(null=False, blank=False)
    category      = models.CharField(max_length=10, null=False, blank=False, choices=cat_options)
    quantity      = models.IntegerField(validators=[MinValueValidator(1)], default=50)
    status        = models.CharField(max_length=25, null=False, blank=False, choices=type_options, default='defualt')
    ordercount    = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.title


class Order(models.Model):

    # relations attr
    item             = models.ForeignKey('orders.Item', on_delete=models.CASCADE, related_name='ordereditem')
    cart             = models.ForeignKey('users.Cart', on_delete=models.CASCADE, related_name='cart', null=True, blank=True, db_constraint=False)
    # premitive attrs
    orderid          = models.CharField(max_length=7, null=False, blank=False, unique=True, default='#123456')
    created_on       = models.DateTimeField(auto_now_add=True)
    quantity         = models.IntegerField(validators=[MinValueValidator(1)])
    price            = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    size             = models.CharField(max_length=10, null=False, blank=False)
    type             = models.CharField(max_length=10, null=False, blank=False)
 
    class Meta:
        verbose_name = "order"
        verbose_name_plural = "Orders"
          
    def __str__(self):
        return f'Order {self.orderid}: {self.created_on.strftime("%b %d %Y %I:%M %p")}'



    
class Payment(models.Model):
    method_choices = [
        ('Mastercard', 'Mastercard'),
        ('Visa', 'Visa'),
        ('Bank Account', 'Bank Account'),
        ('Paypal', 'Paypal')
    ]
    paid_choices = [
        ('upon receipt', 'upon receipt'),
        ('paid', 'paid')
    ]
    status_choices = [
        ('Delevering', 'Delevering'),
        ('Delivered', 'Delivered')
    ]
    # relations
    payer                 = models.ForeignKey('users.User', related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    orders                = models.ManyToManyField('orders.Order', related_name='orders')
    # premetive attrs
    code                  = models.CharField(max_length=9, null=False, blank=False, default=f'#18776527')
    date                  = models.DateTimeField(auto_now_add=True)
    method                = models.CharField(max_length=15, null=False, blank=False, default='Mastercard', choices=method_choices)
    paid                  = models.CharField(max_length=15, default='upon receipt', choices=paid_choices)
    status                = models.CharField(max_length=15, default='Delevering', choices=status_choices)
    price                 = models.DecimalField(max_digits=10, decimal_places=2, default=0) 

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f'{self.code}'



class Tables(models.Model):

    # relations
    reciever              = models.ForeignKey('users.User', related_name='reciever', on_delete=models.CASCADE, null=True, blank=True)
    # premetive attrs
    name                  = models.CharField(max_length=100, null=False, blank=False)              
    email                 = models.CharField(max_length=50, null=True, blank=True)
    phone                 =  models.CharField(max_length=11, null=False, blank=False)
    count                 = models.IntegerField()
    date                  = models.DateField(auto_now_add=True)
    time                  = models.TimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = "table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return f'Table recieved from {self.name}'
