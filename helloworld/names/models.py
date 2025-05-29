from django.db import models

    
class myuser(models.Model):
    username=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255,null=False)
    def __str__(self):
        return self.username

class Message(models.Model):
    sender = models.ForeignKey(myuser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(myuser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
