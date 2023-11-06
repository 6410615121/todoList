from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name ='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]
