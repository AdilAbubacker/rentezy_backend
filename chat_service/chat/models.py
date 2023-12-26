from django.db import models

class Message(models.Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: user {self.sender} To: {self.receiver} - {self.timestamp}"