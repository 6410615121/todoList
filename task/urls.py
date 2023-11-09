from django.urls import path
from . import views

urlpatterns = [
    path('tasklist/', views.individual_tasklist, name='individual_tasklist'),   # link to individual_tasklist in views.py
    path('taskadd/', views.task_add, name='task_add'),   # link to task_add in views.py
    path('individual_taskAdd/', views.individual_taskAdd, name = "individual_taskadd"), # link to individual_taskadd in views.py
    path('pastduetask/', views.individual_past_tasklist, name = "individual_past_tasklist"),
    path('completedtask/', views.individual_com_tasklist, name = "individual_com_tasklist"),
]
