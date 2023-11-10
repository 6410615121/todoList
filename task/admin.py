from django.contrib import admin
from .models import Task ,Individual_Task
# Register your models here.
class Individual(admin.ModelAdmin):
    list_display = ['task_title' ]

class task(admin.ModelAdmin):
    list_display = ['task_title' ]
admin.site.register(Task,task)
admin.site.register(Individual_Task,Individual)