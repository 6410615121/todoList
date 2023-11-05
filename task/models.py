from django.db import models
from user.models import todoUser , Friend
from project.models import Project
import uuid
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    Project_ID = models.ForeignKey(Project, on_delete=models.CASCADE)
    Teamleader_ID = models.ForeignKey(todoUser, on_delete=models.CASCADE)
    TeamUser_ID = models.ManyToManyField(Friend) 
    task_title = models.CharField(max_length=64)
    Entry_Date = models.DateTimeField(auto_now=True)
    Due_Date =   models.DateTimeField(default=timezone.now)
    Finish_Date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False,editable=False)
    description = models.TextField(default="No description")

class Individual_Task(models.Model):
    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    User_ID = models.ForeignKey(todoUser, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=64)
    Entry_Date = models.DateTimeField(auto_now=True)
    Due_Date =   models.DateTimeField(default=timezone.now)
    Finish_Date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False,editable=False)
    description = models.TextField(default="No description")


    
   
    

