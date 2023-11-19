from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name ='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('sendfriendrequest/<uuid:userID>/' ,views.send_friend_request ,name="send_friend_request"),
    path('acceptfriend/' ,views.accept_friend_request ,name="accept_friend_request"),
    path('myfriends/' ,views.friend_list ,name="friend_list"),
    path('searchuser/' ,views.find_user ,name="find_user"),
    path('friendrequest/' ,views.friend_request ,name="friend request"),
    path('sendrequest/' ,views.show_send_request ,name="show_send_request"),
]
