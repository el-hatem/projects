import random as rd
from django.template.defaulttags import register
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View
from threading import Timer
# custom modules
from orders.models import (
    Payment
)
from orders.models import (
    Item, Order
)
from users.models import (
    User, Rating
)


# Create your views here.

# All Orders view
class OrdersView(View):
    template_name = './orders/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        timer = Timer(60, change_status)
        timer.start()
        return super(OrdersView, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        user = User.objects.get(username=request.user.username)
        favs = user.favourites.all()
        cart = user.cart
        orders = Order.objects.filter(cart=cart).all()
        for i in items:
            if i.quantity == 0:
                i.status = 'out of stock'
        
        return render(request, self.template_name, {'items': items, 'orders': orders, 'favs': favs})
            


# Payment view
class PaymentView(View):
    # template_name = './orders/index.html'
        
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        paid = request.POST.get('paid', 'paid')
        cart = user.cart
        card = user.card
        orders = Order.objects.filter(cart=cart).all()
        
        if paid == 'paid' and cart.totalprice < card.budget:
            payment = Payment.objects.create(code=f"#{rd.randint(10000000, 99999999)}", payer=user)
            payment.orders.set(orders)
            payment.paid = paid
            cart.totalprice += 25
            payment.price = cart.totalprice
            payment.save()
            card.budget -= cart.totalprice
            card.save()
                
            # set objects to default
            cart.totalprice = 0
            if cart.state:
                cart.state = False
            cart.save()
            for order in orders:
                order.cart = None
                order.save()
            messages.success(request, "Payment has been successfully.")
            return redirect(reverse('dashboard:cart')) #redirect(reverse('users:profile') + '#bill')
        elif paid == 'upon receipt':
            payment = Payment.objects.create(code=f"#{rd.randint(10000000, 99999999)}", payer=user)
            payment.orders.set(orders)
            payment.paid = paid
            cart.totalprice += 25
            payment.price = cart.totalprice
            payment.save()

            # set objects to default
            cart.totalprice = 0
            if cart.state:
                cart.state = False
            cart.save()
            for order in orders:
                order.cart = None
                order.save()
            messages.success(request, "Payment has been successfully.")
            return redirect(reverse('dashboard:cart')) #redirect(reverse('users:profile') + '#bill')
        else:
            messages.error(request, "You don't have enough money.")
            return redirect(request.META.get('HTTP_REFERER'))
            


# All Orders view
class OrderItemView(View):
        
    def post(self, request, *args, **kwargs):
        exclude_keys = ['csrfmiddlewaretoken']
        fields = {key: value for key, value in request.POST.items()}
        saved_fields = {k: fields[k] for k in set(list(fields.keys())) - set(exclude_keys)}
        
        orderid = f'#{rd.randint(100000, 999999)}'
        item = Item.objects.get(pk=kwargs['id'])
        currentuser = User.objects.get(username=request.user.username)
        currentcart = currentuser.cart
        if not currentcart.state:
            currentcart.state = True
            currentcart.save()
        
        keys = {k: fields[k] for k in set(list(saved_fields.keys())) - set(['quantity'])}
        orders = Order.objects.filter(item=item, cart=currentcart, **keys).all()
        if len(orders) == 1:
            orders[0].quantity += int(saved_fields['quantity'])
            orders[0].price = int(orders[0].quantity) * float(item.price)
            orders[0].save()
        else:
            orderprice = int(saved_fields['quantity']) * float(item.price)
            currentorder = Order(orderid=orderid, item=item, cart=currentcart, price=orderprice, **saved_fields)
            currentorder.save()
            
        user = User.objects.get(username=request.user.username)
        cart = user.cart
        listorders = Order.objects.filter(cart=cart).all()
        cart.totalprice = sum([o.price for o in listorders])
        cart.save()
        return redirect(request.META.get('HTTP_REFERER'))


@require_http_methods(["POST"])
@login_required
def removeorder(request, id):
    order = Order.objects.get(pk=id)
    order.delete()
    return redirect('dashboard:cart')

@require_http_methods(["POST"])
@login_required
def reviewitem(request, id):
    exclude_keys = ['csrfmiddlewaretoken']
    fields = {key: value for key, value in request.POST.items()}
    saved_fields = {k: fields[k] for k in set(list(fields.keys())) - set(exclude_keys)}
    user = User.objects.get(username=request.user.username)
    item = Item.objects.get(pk=id)
    review = Rating(item=item, user=user, **saved_fields)
    review.save()
    return redirect(request.META.get('HTTP_REFERER'))

    
def change_status():
    items = Item.objects.filter(quantity__gt=0).exclude(status='out of stock').all().order_by('?')[:10]
    options = ['default', 'sale']
    for i in items:
        i.status = rd.choice(options)
        i.save()

    

@register.filter
def ratesavg(rates):
    try:
        return sum([r.rate for r in rates]) // len(rates)
    except:
        return 0
        

@register.filter
def inrange(loop):
    return range(loop)

@register.filter
def diffrange(loop):
    return range(5-loop)