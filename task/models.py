from django.db import models
from user.models import todoUser 
from project.models import Project 
import uuid
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    Teamleader = models.ForeignKey(todoUser, on_delete=models.CASCADE)
    TeamUser = models.ForeignKey(todoUser, on_delete=models.CASCADE,related_name = 'assignedtask') 
    task_title = models.CharField(max_length=64)
    Entry_Date = models.DateTimeField(auto_now=True)
    Due_Date =   models.DateTimeField(default=timezone.now)
    Finish_Date = models.DateTimeField(default=timezone.now)
    achieve = models.BooleanField(default=False)
    description = models.TextField(default="No description")
    file = models.FileField(null=True,blank=True)
    
    CATEGORY_CHOICES = (
        ('due', 'due'),
        ('pastdue', 'pastdue'),
        ('complete', 'complete'),
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='due',  # Set a default to be due
    )

    @property
    def time_difference(self):
        return self.Due_Date - timezone.now()


class Individual_Task(models.Model):
    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    User = models.ForeignKey(todoUser, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=64)
    Entry_Date = models.DateTimeField(auto_now=True)
    Due_Date =   models.DateTimeField(default=timezone.now)
    Finish_Date = models.DateTimeField(default=timezone.now)
    achieve = models.BooleanField(default=False)
    description = models.TextField(default="No description")
    file = models.FileField(null=True,blank=True)
    CATEGORY_CHOICES = (
        ('due', 'due'),
        ('pastdue', 'pastdue'),
        ('complete', 'complete'),
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='due',  # Set a default to be due
    )

    @property
    def time_difference(self):
        diff =  self.Due_Date - timezone.now()
        days = diff.days
        seconds = diff.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        
        return f"{days} days  {hours}:{minutes}:{seconds}"
     
    
   
    

