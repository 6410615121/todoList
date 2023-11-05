from django.db import models

# Create your models here.
from django.db import models
import uuid
from user.models import Customer , Friend



# Create your models here.
class Project(models.Model):
    Project_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    Project_name = models.CharField(max_length=64)
    
    

class Team(models.Model):
    Project_ID = models.ForeignKey(Project, on_delete=models.CASCADE)
    Team_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    Team_name = models.CharField(max_length=64)
    TeamLeader_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    TeamUser_ID = models.ManyToManyField(Friend)

    


    

