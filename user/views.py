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


def friend_request(request):   # this function will render html that show all request from other users send request to me 
    to_user = todoUser.objects.get(user=request.user)
    
    all_friend_request =  Friend_request.objects.filter(To_user = to_user)
    context = {
        'friends_request': all_friend_request,  
    }
    return render(request,'user/acc_friendrequest.html',context)



def show_send_request(request):
    from_user = todoUser.objects.get(user=request.user)
    all_friend_request =  Friend_request.objects.filter(From_user = from_user)
    context = {
        'friends_request': all_friend_request,  
        }
    return render(request,'user/sendfriendrequest.html',context)





def send_friend_request(request ,userID):
    from_user = todoUser.objects.get(user=request.user)
    to_user = todoUser.objects.get(todoUser_ID=userID)
    Friend_request.objects.get_or_create( From_user = from_user ,To_user = to_user )
    
    return show_send_request(request)
    
    


def accept_friend_request(request):
    
    user_profile = request.user
    id = todoUser.objects.get(user=user_profile)
    friend_request = Friend_request.objects.get(To_user = id)  # other users send to me 
    if friend_request.To_user == id:
        friend_request.To_user.friends.add(friend_request.From_user)
        friend_request.From_user.friends.add(friend_request.To_user)
        friend_request.delete()
        return friend_list(request)
        
    

def friend_list(request):
    myfriend = todoUser.objects.get(user=request.user).friends.all()
    user_profile = request.user
    myuser = todoUser.objects.get(user=user_profile)
    context = {
        'friends': myfriend,  
        'myuser' : myuser
    }
    return render(request, 'user/friendlist.html',context)


def find_user(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        try:
            user_instance = User.objects.get(username=user)
            user = todoUser.objects.get(user= user_instance)
            context = {
                'user': user,  
        }
            return render(request, 'user/detailuser.html',context)
        except:
            messages.error(request, 'There is no user')

        


    return render(request, 'user/finduser.html')