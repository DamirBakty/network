from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Chat(models.Model):
    user = models.ManyToManyField(to=User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(to=User, related_name='messages', on_delete=models.DO_NOTHING)
    chat = models.ForeignKey(to=Chat, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
