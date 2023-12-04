from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name ='about'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('editmyaccount/', views.editprofile, name='editprofile'),
    path('logout/', views.logout_view, name='logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('sendfriendrequest/<uuid:userID>/' ,views.send_friend_request ,name="send_friend_request"),
    path('acceptfriend/<uuid:userID>/' ,views.accept_friend_request ,name="accept_friend_request"),
    path('myfriends/' ,views.friend_list ,name="friend_list"),
    path('searchuser/' ,views.find_user ,name="find_user"),
    path('friendrequest/' ,views.friend_request ,name="friend request"),
    path('sendrequest/' ,views.show_send_request ,name="show_send_request"),
    path('deletefriend/<uuid:userID>/' ,views.delete_friend ,name="delete_friend"),
    path('unsend/<uuid:userID>/' ,views.unsend ,name="unsend"),
]
