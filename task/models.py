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
    def time_difference_format(self):
        if self.achieve:
            return "Completed"

        time_diff = self.Due_Date - timezone.now()

        is_negative = time_diff.total_seconds() < 0

        days, seconds = divmod(abs(time_diff.seconds), 86400)  # 86400 seconds in a day
        hours, remainder = divmod(seconds, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute

        if days > 0:
            formatted_time = f"{days} days, {hours} hours, {minutes} minutes "
        elif hours > 0:
            formatted_time = f"{hours} hours, {minutes} minutes "
        else:
            formatted_time = f"{minutes} minutes "

        return "Late" if is_negative else formatted_time


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
    def time_difference_format(self):
        if self.achieve:
            return "Completed"

        time_diff = self.Due_Date - timezone.now()

        is_negative = time_diff.total_seconds() < 0

        days, seconds = divmod(abs(time_diff.seconds), 86400)  # 86400 seconds in a day
        hours, remainder = divmod(seconds, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute

        if days > 0:
            formatted_time = f"{days} days, {hours} hours, {minutes} minutes "
        elif hours > 0:
            formatted_time = f"{hours} hours, {minutes} minutes "
        else:
            formatted_time = f"{minutes} minutes "

        return "Late" if is_negative else formatted_time

     
    
   
    

