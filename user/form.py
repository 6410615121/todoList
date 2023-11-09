from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter your Firstname'}))
    last_name = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter your Lastname'}))
    email = forms.EmailField(max_length=254, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password',)
        
    
        
    