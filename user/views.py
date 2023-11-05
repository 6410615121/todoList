from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .form import RegistrationForm
from .models import todoUser

# Create your views here.

def about(request):
    return render(request, 'user/about.html') 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new User instance and link it to the Customer
            user = form.save()
            

            todoUser.objects.create(user=user ,Firstname=user.first_name, Lastname=user.last_name )
            
            # Log the user in after registration if needed
            # ...
    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', {'form': form})
    