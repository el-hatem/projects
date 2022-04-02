from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .forms import (
    ActiveListingsForm, EditListingsForm
)
from .models import (
    ActiveListings, Category, Bid
)
from users.models import (
    User, Comments
)


def home(request):
    template_name = "auctions/index.html"
    active_lists = ActiveListings.objects.all()
    return render(request, template_name, {"lists": active_lists})


class IndexView(View):
    template_name = "auctions/index.html"

    def get(self, request, *args, **kwargs):
        active_lists = ActiveListings.objects.filter(state=True).all()
        return render(request, self.template_name, {"lists": active_lists})


class CreateView(View):
    template_name = "auctions/create.html"

    def get(self, request, *args, **kwargs):
        form = ActiveListingsForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = ActiveListingsForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            category_name = form.cleaned_data['category']
            if not category_name:
                category = Category.objects.get(name='unknown')
                instance.category = category

            user = User.objects.get(username=request.user)
            instance.user = user
            instance.save()
            bid = Bid(listing=instance)
            bid.save()
            messages.success(request, "Listing has been created successfully. create another one?")
            form = ActiveListingsForm()
            return render(request, self.template_name, {"form": form})

        return render(request, self.template_name, {"form": form})


class EditView(View):
    template_name = "auctions/edit.html"

    def get(self, request, *args, **kwargs):
        listing = ActiveListings.objects.get(pk=kwargs['id'])
        if request.user == listing.user:
            form = EditListingsForm(initial={
                "title": listing.title,
                "description": listing.description,
                'category': listing.category,
                "image_url": listing.image_url,
            })
            return render(request, self.template_name, {"form": form, "list": listing})
        else:
            return HttpResponse('error 505: forbidden go back to <a href="/"> Home </a>.')

    def post(self, request, *args, **kwargs):
        listing = ActiveListings.objects.get(pk=kwargs['id'])
        form = EditListingsForm(request.POST, instance=listing)

        if form.is_valid():
            category_name = form.cleaned_data['category']
            if not category_name:
                category = Category.objects.get(name='unknown')
                listing.category = category
            form.save()
            return redirect('auctions:listing', id=kwargs['id'])

        return render(request, self.template_name, {"form": form, "list": listing})


@method_decorator(login_required, name='post')
class ListingView(View):
    template_name = "auctions/listing.html"

    def get(self, request, *args, **kwargs):
        listing = ActiveListings.objects.get(pk=kwargs['id'])
        comments = Comments.objects.filter(listing=listing).all()
        bid = Bid.objects.get(listing=listing)
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            watch_lists = user.watched_list.all()
            return render(request, self.template_name, {
                "list": listing, "comments": comments, "watch_lists": watch_lists, "bid": bid
            })
        return render(request, self.template_name, {
            "list": listing, "comments": comments, "bid": bid
        })

    def post(self, request, *args, **kwargs):
        list_id = request.POST['list-id']
        user = User.objects.get(username=request.user)
        listing = ActiveListings.objects.get(id=list_id)
        comments = Comments.objects.filter(listing=listing).all()
        description = request.POST['comment']

        if len(description) <= 0:
            messages.error(request, "invalid empty comment")
            return render(request, self.template_name, {
                "list": listing,
                "comments": comments
            })
        else:
            comment = Comments(description=description, listing=listing, user=user)
            comment.save()

        return redirect('auctions:listing', id=list_id)


def get_category(request, name):
    template_name = 'auctions/index.html'
    category = Category.objects.get(name=name)
    lists = ActiveListings.objects.filter(category=category).all()
    return render(request, template_name, {"lists": lists})


def get_categories(request):
    template_name = 'auctions/categories.html'
    categories = Category.objects.all()
    return render(request, template_name, {"categories": categories})


@login_required(login_url="users:login")
def close_bid(request, list_id):
    listing = ActiveListings.objects.get(pk=list_id)
    if request.user == listing.user:
        listing.state = False
        listing.save()
        return redirect('auctions:index')
    else:
        return HttpResponse('error 505: forbidden go back to <a href="/"> Home </a>.')


@login_required(login_url="users:login")
def modify_watchlist(request, list_id):
    listing = ActiveListings.objects.filter(pk=list_id)
    state = request.GET['state']
    user = User.objects.get(username=request.user.username)
    watch_lists = user.watched_list.all()

    if listing[0] in watch_lists and state == "False":
        user.watched_list.set(user.watched_list.difference(listing))
        user.save()
    elif listing[0] not in watch_lists and state == "True":
        user.watched_list.set(watch_lists.union(listing))
        user.save()
    return redirect('auctions:listing', id=list_id)


@require_http_methods('POST')
@login_required(login_url="users:login")
def post_bid(request, list_id):
    listing = ActiveListings.objects.get(pk=list_id)

    if request.POST['bid'] != "":
        price = Decimal(request.POST['bid'])
        if price > listing.price:
            bid = Bid.objects.get(listing=listing)
            listing.price = price
            bid.winner = request.user
            bid.nbids += 1
            listing.save()
            bid.save()
            messages.success(request, "bid has successfully added!")
            return redirect('auctions:listing', id=list_id)
        else:
            messages.error(request, f"bid must be more than {listing.price}$")
            return redirect('auctions:listing', id=list_id)
    else:
        messages.error(request, "bid must have a value")
        return redirect('auctions:listing', id=list_id)
