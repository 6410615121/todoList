from django.urls import path
from . import views

urlpatterns = [
    path('projectAdd/', views.projectAdd, name ='projectAdd'),
    path('Myproject/', views.ProjectList, name ='ProjectList'),
    path('<uuid:project_id>/', views.project_detail, name='project_detail'),
    path('tasks/<uuid:task_id>/', views.project_task_detail, name='project_task_detail'),
    path('tasks/<uuid:task_id>/submit/', views.submit,name='project_task_submit'),
    path('tasks/<uuid:task_id>/mask_submit/', views.mask_submit,name='mask_submit'),
    path('tasks/<uuid:task_id>/del', views.delete_project_task, name='delete_project_task'),
    path('tasks/<uuid:task_id>/edit', views.project_task_edit, name='project_task_edit'),
    path('<uuid:project_id>/edit',views.project_edit, name="project_edit"),
    path('<uuid:project_id>/delete',views.delete_project, name="project_delete"),
]
