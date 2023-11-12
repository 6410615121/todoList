from django.shortcuts import render, redirect ,HttpResponseRedirect 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .form import RegistrationForm
from .models import todoUser ,Friend_request
from django.contrib.auth import authenticate, login ,logout

# Create your views here.

def about(request):
    return render(request, 'user/about.html') 

def homepage(request):
    return render(request, 'user/homepage.html') 

from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'user/login.html')

    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return render(request, 'user/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new User instance and link it to the Customer
            user = form.save()
            todo_user = todoUser.objects.create(user=user ,Firstname=user.first_name, Lastname=user.last_name )   
            todo_user.save()  
            return HttpResponseRedirect(reverse('login'))   
    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', {'form': form})


def send_friend_request(request ,userID):
    from_user = todoUser.objects.get(user=request.user)
    to_user = todoUser.objects.get(todoUser_ID=userID)
    friend_request ,created = Friend_request.objects.get_or_create( From_user = from_user ,To_user = to_user )
    if created:
        return redirect('homepage')
    else:
        return render(request, 'user/already_sentrequest.html')


def accept_friend_request(request ,userID):
    friend_request = Friend_request.objects.get(From_user = userID)
    user_profile = request.user
    id = todoUser.objects.get(user=user_profile)
    if friend_request.To_user == id:
        friend_request.To_user.friends.add(friend_request.From_user)
        friend_request.From_user.friends.add(friend_request.To_user)
        friend_request.delete()
        return render(request, 'user/register.html') # waiting html
    