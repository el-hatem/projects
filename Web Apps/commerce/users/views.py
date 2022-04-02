from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import User
from auctions.models import ActiveListings
from .forms import UserForm


class LoginView(View):
	template_name = "users/login.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		if user:
			login(request, user)
			return redirect("auctions:index")
		else:
			return render(request, self.template_name, {
				"message": "Invalid username and/or password."
			})


class RegisterView(View):
	template_name = "users/register.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]

		if len(email) <= 0:
			return render(request, self.template_name, {
				"message": "email field is empty."
			})

		if password != confirmation:
			return render(request, self.template_name, {
				"message": "Passwords must match."
			})
		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, self.template_name, {
				"message": "Username already taken."
			})

		return redirect("auctions:index")


class EditSittingsView(View):
	template_name = "users/settings.html"

	def get(self, request, *args, **kwargs):
		form = UserForm()
		return render(request, self.template_name, {
			"form": form
		})

	def post(self, request, *args, **kwargs):
		return redirect("auctions:index")


@login_required(login_url="users:login")
def owned_list(request):
	template_name = 'auctions/index.html'
	user = User.objects.get(username=request.user)
	lists = ActiveListings.objects.filter(user=user).all()
	return render(request, template_name, {"lists": lists})


@login_required(login_url="users:login")
def watch_list(request):
	template_name = 'auctions/index.html'
	user = User.objects.get(username=request.user)
	lists = user.watched_list.all()
	return render(request, template_name, {"lists": lists})


def logout_view(request):
	logout(request)
	return redirect("auctions:index")
