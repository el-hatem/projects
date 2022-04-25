import random as rd
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from threading import Timer
from django.contrib import messages
from users.models import (
    User, Cart, Card
)
from orders.models import (
    Item, Payment
)
# from users.models import User
# Create your views here.


# Login view
class Login(View):
    template_name = './users/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard:home")
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, self.template_name)


# Register view
class Register(View):
    template_name = './users/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        exclude_keys = ['confirm_password', 'csrfmiddlewaretoken']
        fields = {key: value for key, value in request.POST.items()}
        saved_fields = {k: fields[k] for k in set(list(fields.keys())) - set(exclude_keys)}
        
        # dynamic check empty fields
        for k, v in fields.items():
            if len(v) <= 0:
                messages.error(request, f"{k} field is empty.")
                return render(request, self.template_name)
        if fields['password'] != fields['confirm_password']:
            messages.error(request, "passwords must be identical.")
            return render(request, self.template_name)
        # Attempt to create new user
        try:
            
            cart = Cart()
            cart.save()
            user = User.objects.create_user(**saved_fields, cart=cart)
            user.save()
            return redirect("users:login")
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, self.template_name)
        

# Register view
class Settings(View):
    template_name = './users/profile_settings.html'
    
    def dispatch(self, request, *args, **kwargs):
        timerpay = Timer(10, change_payment_status, args=[request])
        timerpay.start()
        return super(Settings, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        payments = Payment.objects.filter(payer=user).all()
        return render(request, self.template_name, {'payments': payments})

    
@login_required(login_url="users:login")
def addwatchlist(request, id):
    item = Item.objects.filter(pk=id)

    user = User.objects.get(username=request.user.username)
    favourites = user.favourites.all()
    if item[0] not in favourites:
        user.favourites.set(favourites.union(item))
        user.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="users:login")
def removewatchlist(request, id):
    item = Item.objects.filter(pk=id)
    user = User.objects.get(username=request.user.username)
    favourites = user.favourites.all()
    if item[0] in favourites:
        user.favourites.set(user.favourites.difference(item))
        user.save()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url="users:login")
@require_http_methods("POST")
def add_card(request):
    inputs = { key: value
            for key, value in request.POST.items()
            if key in ['owner', 'card-number', 'expired-date', 'cvv']}
    inputs['expired-date'] = inputs['expired-date'] + '-1'
    
    try:
        card = Card.objects.get(cardnumber=inputs['card-number'])
        messages.error(request, "This card already exists for another user.")
        return redirect(reverse('users:profile') + '#bill')
    except:
        user = User.objects.get(username=request.user.username)
        try:
            user.card.delete()
            card = Card(cardowner=inputs['owner'], cardnumber=inputs['card-number'],
                         expired_date=inputs['expired-date'], cvv=inputs['cvv'], budget=rd.uniform(300.80, 2400.90))
            card.save()
            user.card = card
            user.save()
        except:
            card = Card(cardowner=inputs['owner'], cardnumber=inputs['card-number'],
                         expired_date=inputs['expired-date'], cvv=inputs['cvv'], budget=rd.uniform(300.80, 2400.90))
            card.save()
            user.card = card
            user.save()
        messages.success(request, "Card added successfully")
        return redirect(reverse("users:profile")+"#bill")


@login_required(login_url="users:login")
@require_http_methods("POST")
def delete_card(request):
    exclude_keys = ['csrfmiddlewaretoken']
    fields = {key: value for key, value in request.POST.items()}
    saved_fields = {k: fields[k] for k in set(list(fields.keys())) - set(exclude_keys)}
    user = User.objects.get(username=request.user.username)
    auth = authenticate(request, username=user.username, password=saved_fields['user-password'])
    if auth:
        try:
            user.card.delete()
            messages.success(request, "Card deleted successfully")
            return redirect(reverse("users:profile")+"#bill")
        except:
            messages.error(request, "No added Cards to delete")
            return redirect(reverse("users:profile")+"#bill")
    messages.error(request, "wrong password please try again!!")
    return redirect(request.META.get('HTTP_REFERER'))

# logout
@login_required(login_url="users:login")
def logout_view(request):
    logout(request)
    return redirect("users:logout")



def change_payment_status(request):
    user = User.objects.get(username=request.user.username)
    payments = Payment.objects.filter(payer=user).all()
    
    for payment in payments:
        payment.status = 'Delivered'
        payment.paid = 'paid'
        payment.save()
    