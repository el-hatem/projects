from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from chat.models import UserProfile, chatMessages

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
        help_texts = {
            'username': None,
            'password': None,
            'password': None,
        }



class MessageForm(forms.ModelForm):
    class Meta:
        model = chatMessages
        fields = ['user_from', 'user_to', 'message', 'file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }




class UpdateProfileForm(forms.ModelForm):
        
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdateUserForm(forms.ModelForm):
        
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        help_texts = {
            'username': None,
        }

