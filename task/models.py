from django.db import models
from user.models import todoUser 
from project.models import Project 
import uuid
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    Project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='tasks_project')
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
    
    @property
    def time_difference_format(self):
        if self.achieve:
            return "Completed"

        time_diff = self.Due_Date - timezone.now()
        
        # Check if time_diff is negative
        is_negative = time_diff.total_seconds() < 0
        
        # Calculate days, hours, minutes
        days, seconds = divmod(abs(time_diff.seconds), 86400)  # 86400 seconds in a day
        hours, remainder = divmod(seconds, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute
        
        # Format the result
        if days > 0:
            formatted_time = f"{days} days, {hours} hours, {minutes} minutes left"
        elif hours > 0:
            formatted_time = f"{hours} hours, {minutes} minutes left"
        else:
            formatted_time = f"{minutes} minutes left"
            
        # Return "Late" if time_diff is negative
        return "Late" if is_negative else formatted_time

    
    
    
    def __str__(self) -> str:
        return self.task_title


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
     
    
   
    

