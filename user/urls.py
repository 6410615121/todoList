from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name ='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('friendrequest/<uuid:userID>/' ,views.send_friend_request ,name="send_friend_request"),
    path('acceptfriend/<uuid:userID>/' ,views.accept_friend_request ,name="accept_friend_request"),
]
