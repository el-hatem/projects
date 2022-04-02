from django import forms
from .models import User 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
	Submit, Layout
)


class UserForm(forms.ModelForm):
	confirm = forms.CharField(max_length=128, widget=forms.PasswordInput)
	password = forms.CharField(max_length=128, widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password')
