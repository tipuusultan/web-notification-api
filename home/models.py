from django.db import models
from django.utils import timezone

# Create your models here.

class UserFCMToken(models.Model):
    """Model to store user FCM tokens for push notifications"""
    token = models.CharField(max_length=500, unique=True)
    user_agent = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Token: {self.token[:50]}..."

    class Meta:
        db_table = 'user_fcm_tokens'

class ScheduledNotification(models.Model):
    """Model to store scheduled notifications"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    fcm_token = models.ForeignKey(UserFCMToken, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.fcm_token.token[:30]}..."
    
    class Meta:
        db_table = 'scheduled_notifications'
        ordering = ['scheduled_at']
