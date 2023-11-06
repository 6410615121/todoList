# Create your models here.
from django.db import models
import uuid
from user.models import todoUser



# Create your models here.
class Project(models.Model):
    Project_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    Project_name = models.CharField(max_length=64)

    TeamLeader = models.ForeignKey(todoUser, on_delete=models.CASCADE, related_name="TeamLeader",null=True)
    TeamMember = models.ManyToManyField(todoUser, related_name="TeamMember")
    
    def __str__(self):
        return self.Project_name
    

    

    
    

    


    

