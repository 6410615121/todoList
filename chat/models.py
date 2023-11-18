from django.db import models
from user.models import todoUser

# Create your models here.
from django.db import models

class ChatMessage(models.Model):
    user = models.ForeignKey(todoUser , on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)