# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    # 添加自定义字段
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    introduction = models.CharField(max_length=400, blank=True, default='这个家伙很懒，还没有添加简介~~')

class Friendship(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='friendship_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

class PrivateMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    request_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address} - {self.request_time}"

class BannedUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ban_end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - Banned until {self.ban_end_time}"
class BannedIP(models.Model):
    ip_address = models.GenericIPAddressField()
    ban_end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.ip_address} - Banned until {self.ban_end_time}"