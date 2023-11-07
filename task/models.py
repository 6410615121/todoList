from django.db import models
from user.models import todoUser
from project.models import Project#,Team
import uuid
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    TaskOwner = models.ForeignKey(todoUser, on_delete=models.CASCADE, related_name="owned_tasks",null=True) 

    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    task_title = models.CharField(max_length=64)
    Entry_Date = models.DateTimeField(auto_now=True)
    Due_Date =   models.DateTimeField(default=timezone.now)
    Finish_Date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False,editable=False)
    description = models.TextField(default="No description")
    file = models.FileField(null=True,blank=True)

    def __str__(self):
        return f"title: {self.task_title}////Task Owner: {self.TaskOwner.Firstname} {self.TaskOwner.Lastname}"



class Individual_Task(models.Model):
    User = models.ForeignKey(todoUser, on_delete=models.CASCADE, related_name="individual_tasks")

    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    task_title = models.CharField(max_length=64)
    Entry_Date = models.DateTimeField(auto_now=True)
    Due_Date =   models.DateTimeField(default=timezone.now)
    Finish_Date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False,editable=False)
    description = models.TextField(default="No description")
    file = models.FileField(null=True,blank=True)





    
   
    

