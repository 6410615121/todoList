from django.db import models
from django.contrib.auth.models import User 
import uuid

# Create your models here.
class todoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    todoUser_ID = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    Firstname = models.CharField(max_length=50 )
    Lastname = models.CharField(max_length=50 )
    image_field = models.ImageField(upload_to='user_images/', default='user_images/defaultprofile.jpg')
    

    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f"{self.Firstname} {self.Lastname}" 
    


    


class Friend_request(models.Model):
    From_user = models.ForeignKey(todoUser,related_name="from_user", on_delete=models.CASCADE)
    To_user = models.ForeignKey(todoUser,related_name= "to_user", on_delete=models.CASCADE)

class Forget_pass(models.Model):
   forget_ID = models.UUIDField(default=uuid.uuid4, primary_key=True)
   user = models.ForeignKey(User, on_delete=models.CASCADE )


