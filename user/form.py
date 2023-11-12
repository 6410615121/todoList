from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True )
    last_name = forms.CharField(max_length=30, required=True )
    email = forms.EmailField(max_length=254, required=True )
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Set placeholder for all fields
        for field_name, field in self.fields.items():
            if field_name == "password2":
                field.widget.attrs['placeholder'] = f'Password confirmation'
            else:
                field.widget.attrs['placeholder'] = f'Enter your {field_name.capitalize()}'
    
        
    