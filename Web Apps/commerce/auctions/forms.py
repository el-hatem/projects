from django import forms 
from .models import (
	ActiveListings
)


class ActiveListingsForm(forms.ModelForm):
	class Meta:
		model = ActiveListings
		fields = ('title', 'price', 'description', 'category', 'image_url',)


class EditListingsForm(forms.ModelForm):
	class Meta:
		model = ActiveListings
		fields = ('title', 'description', 'category', 'image_url',)
