from django.urls import path
from . import views

urlpatterns = [
    path('tasklist/', views.individual_tasklist, name='individual_tasklist'),   # link to individual_tasklist in views.py
    path('taskadd/<uuid:project_ID>/', views.task_add, name='task_add'),   # link to task_add in views.py
    path('individual_taskAdd/', views.individual_taskAdd, name = "individual_taskadd"), # link to individual_taskadd in views.py
    path('pastduetask/', views.individual_past_tasklist, name = "individual_past_tasklist"),
    path('completedtask/', views.individual_com_tasklist, name = "individual_com_tasklist"),
    path('<uuid:task_id>/', views.task_detail, name='task_detail'),
    path('download/<uuid:task_id>/', views.download_file, name='download_file'),
    path('submit/<uuid:task_id>/', views.submit, name='submit'),
    path('del/<uuid:task_id>/', views.delete_individual_task, name='delete_individual_task'),
]
