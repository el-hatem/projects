from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from orders.models import (
    Item, Order, Payment, Tables
)
from users.models import (
    User
)
# Create your views here.

# homepage view
class Homepage(View):
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        main_menu = Item.objects.filter(ordercount__gte=10).all()
        return render(request, self.template_name, {'menu': main_menu})

# menu view
class Menu(View):
    template_name = 'menu.html'
    def get(self, request, *args, **kwargs):
        main_menu = Item.objects.filter(ordercount__gte=10).all()
        return render(request, self.template_name, {'menu': main_menu})


# menu view
class CartView(View):
    template_name = 'cart.html'
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        cart = user.cart
        listorders = Order.objects.filter(cart=cart).all()
        cart.totalprice = sum([o.price for o in listorders])
        cart.save()
        return render(request, self.template_name, {'orders': listorders, 'cart': cart})




# Ordertable view
class OrdertableView(View):
    template_name = 'order_table.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        exclude_keys = ['csrfmiddlewaretoken']
        fields = {key: value for key, value in request.POST.items()}
        saved_fields = {k: fields[k] for k in set(list(fields.keys())) - set(exclude_keys)}
        user = User.objects.get(username=request.user.username)
        table = Tables.objects.filter(date=saved_fields['date'], time=saved_fields['time']).all()
        if not table:
            table = Tables(**saved_fields, reciever=user)
            table.save()
            messages.success(request, "Table has been recervied successfully.")
            return render(request, self.template_name)
        else:
            messages.error(request, "Table already reserved.")
            return render(request, self.template_name)
            

# menu view
class WatchlistView(View):
    template_name = 'watchlist.html'
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        favs = user.favourites.all()
        return render(request, self.template_name, {'favs': favs})
    

# item view
class ItemView(View):
    template_name = 'item.html'
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=kwargs['id'])
        similars = Item.objects.filter(category=item.category)
        user = User.objects.get(username=request.user.username)
        cart = user.cart
        orders = Order.objects.filter(cart=cart).all()
        favs = user.favourites.all()
            
        return render(request, self.template_name, {'item': item, 'similars': similars, 'orders':orders, 'favs': favs})


@login_required(login_url="users:login")
def paymentdetails(request, id):
    payment = Payment.objects.get(pk=id)
    return  render(request, 'payment_details.html', {'payment': payment})


@register.filter
def cutprice(price):
    return price - 25
# about view
class About(View):
    template_name = 'about.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)