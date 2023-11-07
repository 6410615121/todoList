from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .form import RegistrationForm
from .models import todoUser

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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
            redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or any other desired URL
            return redirect('index')
        else:
            # Provide an error message or handle invalid login attempts
            return render(request, 'user/login.html', {'error': 'Invalid username or password'})

    return render(request, 'user/login.html')  # Render the login form


    