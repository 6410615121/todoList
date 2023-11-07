from django.urls import path
from . import views

urlpatterns = [
    path('', views.taskIndex, name='taskIndex'),
    path('taskadd/', views.task_add, name='task_add'),
    path('individual_taskAdd/', views.individual_taskAdd, name = "individual_taskadd"),
    path('taskIndividualList/', views.taskIndividualList, name = 'taskIndividualList'),
    path('taskList', views.taskList, name = "taskList"),
]
