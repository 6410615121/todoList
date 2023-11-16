from django.urls import path
from . import views

urlpatterns = [
    path('projectAdd/', views.projectAdd, name ='projectAdd'),
    path('Myproject/', views.ProjectList, name ='ProjectList'),
    path('<uuid:project_id>/', views.project_detail, name='project_detail'),
    path('tasks/<uuid:task_id>/', views.project_task_detail, name='project_task_detail'),
    path('tasks/<uuid:task_id>/submit/', views.submit,name='project_task_submit'),
    path('tasks/<uuid:task_id>/del', views.delete_project_task, name='delete_project_task'),
]
