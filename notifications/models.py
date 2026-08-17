from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#blueprint for structure of database
class NotificationJob(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    #each variable are columns included in the database
    #and JSON payload

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    recipient_email = models.EmailField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    secret_key = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
