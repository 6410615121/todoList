from django.urls import path
from . import views

urlpatterns = [
    path('projectAdd/', views.projectAdd, name ='projectAdd'),
    path('Myproject/', views.ProjectList, name ='ProjectList'),
    path('<uuid:project_id>/', views.project_detail, name='project_detail'),
]
