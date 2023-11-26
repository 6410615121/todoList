from django.shortcuts import render, redirect ,HttpResponseRedirect 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .form import RegistrationForm
from .models import todoUser ,Friend_request ,Forget_pass
from project.models import Project 
from django.contrib.auth import authenticate, login ,logout
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from task.views import updatetask

# Create your views here.

def about(request):
    return render(request, 'user/about.html') 

@login_required(login_url='login')
def homepage(request):
    todouser = todoUser.objects.get(user = request.user)

    project_obj = Project.objects.filter(TeamMember =  todouser)
    tasks = None
    assignedtask = None
    for t in project_obj:
        tasks = t.tasks_project.all()
        assignedtask = tasks.filter(TeamUser = todouser)

    
    mytask = updatetask(request,"due")
    context = {
        'individualtask' : mytask,
        'assignedtask'   : assignedtask,
    }
    return render(request, 'user/homepage.html',context) 

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

def forgetpass(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)

        mail = Forget_pass.objects.create(user=user)
        content=f"""
            Hello {request.user},

            We received a request to update the password for your account. To reset your password, please click the link below:

            [Password Reset Link:](http://127.0.0.1:8000/{mail.forget_ID}/resetpass/)

            If you did not initiate this request, please ignore this email. Your account security is important to us.

        """

        send_mail(' Password Reset Request', content, settings.EMAIL_HOST_USER,[email])
        return render(request, 'user/login.html')
    
    return render(request, 'user/forgetpass.html')

def resetpass(request,requestID):
    Forget_pass_obj = get_object_or_404(Forget_pass, forget_ID=requestID)

    if request.method == 'POST':
        newpass = request.POST.get('pass1')

        user = Forget_pass_obj.user
        user.set_password(str(newpass))
        user.save()
        Forget_pass_obj.delete()
        return render(request, 'user/login.html')
    
    return render(request, 'user/resetpass.html', {"requestID":requestID,})
    

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('login')

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

@login_required(login_url='login')
def friend_request(request):   # this function will render html that show all request from other users send request to me 
    to_user = todoUser.objects.get(user=request.user)
    
    all_friend_request =  Friend_request.objects.filter(To_user = to_user)
    context = {
        'friends_request': all_friend_request,  
    }
    return render(request,'user/acc_friendrequest.html',context)


@login_required(login_url='login')
def show_send_request(request):
    from_user = todoUser.objects.get(user=request.user)
    all_friend_request =  Friend_request.objects.filter(From_user = from_user)
    context = {
        'friends_request': all_friend_request,  
        }
    return render(request,'user/sendfriendrequest.html',context)




@login_required(login_url='login')
def send_friend_request(request ,userID):
    from_user = todoUser.objects.get(user=request.user)
    to_user = todoUser.objects.get(todoUser_ID=userID)
    Friend_request.objects.get_or_create( From_user = from_user ,To_user = to_user )
    
    return friend_list(request)
    
    

@login_required(login_url='login')
def accept_friend_request(request):
    
    user_profile = request.user
    id = todoUser.objects.get(user=user_profile)
    friend_request = Friend_request.objects.get(To_user = id)  # other users send to me 
    if friend_request.To_user == id:
        friend_request.To_user.friends.add(friend_request.From_user)
        friend_request.From_user.friends.add(friend_request.To_user)
        friend_request.delete()
        return friend_list(request)
        
    
@login_required(login_url='login')
def friend_list(request):
    myfriend = todoUser.objects.get(user=request.user).friends.all()
    user_profile = request.user
    myuser = todoUser.objects.get(user=user_profile)
    context = {
        'friends': myfriend,  
        'myuser' : myuser
    }
    return render(request, 'user/friendlist.html',context)

@login_required(login_url='login')
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


@login_required(login_url='login')
def myaccount(request):

    user = User.objects.get(username = request.user)
    todouser = todoUser.objects.get(user= request.user)
    return render(request, 'user/myaccount.html',{'user':user,'todouser':todouser}) 


@login_required(login_url='login')
def editprofile(request):
    todouser_request = todoUser.objects.get(user=request.user)
    user = User.objects.get(username = request.user)
    if request.method == 'POST':
        # Get the uploaded image from the request
        uploaded_image = request.FILES.get('profile_picture')

        if uploaded_image:
            # Use the original filename of the uploaded image
            filename = uploaded_image.name
            
            # Save the image to the user's profile picture field
            todouser_request.image_field.save(filename, uploaded_image)

        # You can also update other profile fields here if needed
        todouser_request.Firstname = request.POST.get('Firstname')
        todouser_request.Lastname = request.POST.get('Lastname')
        user.email = request.POST.get('Email')
        todouser_request.save()
        user.save()
        return redirect('myaccount')

    return render(request, 'user/editprofile.html', {'todouser': todouser_request})