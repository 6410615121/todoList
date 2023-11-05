from django.db import models
from django.contrib.auth.models import User 
import uuid

# Create your models here.
class todoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,editable=False)
    todoUser_ID = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    Firstname = models.CharField(max_length=50 )
    Lastname = models.CharField(max_length=50 )
    
    def __str__(self):
        return f'Name:{self.user} ID:{self. todoUser_ID}'
    


class Friend(models.Model):
    From_user = models.ForeignKey(todoUser,related_name="from_user", on_delete=models.CASCADE)
    To_user = models.ForeignKey(todoUser,related_name= "to_user", on_delete=models.CASCADE)


