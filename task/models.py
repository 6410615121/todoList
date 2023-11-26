from django.db import models
from user.models import todoUser 
from project.models import Project 
import uuid
from django.utils import timezone
from datetime import timedelta

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
    file = models.FileField(upload_to='user_files/',null=True,blank=True)
    
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
    def time_difference_format(self):
        if self.achieve:
            return "Completed"

        time_diff = max(self.Due_Date - timezone.now(), timedelta())  # Use max to ensure non-negative timedelta
        
        # Calculate days, hours, minutes
        total_seconds = time_diff.total_seconds()
        days = int(total_seconds // 86400)  # 86400 seconds in a day
        hours = int((total_seconds % 86400) // 3600)  # 3600 seconds in an hour
        minutes = int((total_seconds % 3600) // 60)  # 60 seconds in a minute

        # Format the result
        if days > 0:
            formatted_time = f"{days} days, {hours} hours, {minutes} minutes"
        elif hours > 0:
            formatted_time = f"{hours} hours, {minutes} minutes"
        else:
            formatted_time = f"{minutes} minutes"

        # Return "Late" if time_diff is negative
        return "Late" if self.Due_Date < timezone.now() else formatted_time

class Individual_Task(models.Model):
    Task_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    User = models.ForeignKey(todoUser, on_delete=models.CASCADE, related_name='Individual_Task')
    task_title = models.CharField(max_length=64)
    Entry_Date = models.DateTimeField(auto_now=True)
    Due_Date =   models.DateTimeField(default=timezone.now)
    Finish_Date = models.DateTimeField(default=timezone.now)
    achieve = models.BooleanField(default=False)
    description = models.TextField(default="No description")
    file = models.FileField(upload_to='user_files/',null=True,blank=True)
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
    def time_difference_format(self):
        if self.achieve:
            return "Completed"

        time_diff = max(self.Due_Date - timezone.now(), timedelta())  # Use max to ensure non-negative timedelta
        
        # Calculate days, hours, minutes
        total_seconds = time_diff.total_seconds()
        days = int(total_seconds // 86400)  # 86400 seconds in a day
        hours = int((total_seconds % 86400) // 3600)  # 3600 seconds in an hour
        minutes = int((total_seconds % 3600) // 60)  # 60 seconds in a minute

        # Format the result
        if days > 0:
            formatted_time = f"{days} days, {hours} hours, {minutes} minutes"
        elif hours > 0:
            formatted_time = f"{hours} hours, {minutes} minutes"
        else:
            formatted_time = f"{minutes} minutes"

        # Return "Late" if time_diff is negative
        return "Late" if self.Due_Date < timezone.now() else formatted_time



     
    
   
    

