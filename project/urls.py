from django.urls import path
from . import views

urlpatterns = [
    path('projectAdd/', views.projectAdd, name ='projectAdd'),
    path('Myproject/', views.ProjectList, name ='ProjectList'),
]
