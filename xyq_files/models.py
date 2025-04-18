from django.db import models
from django.conf import settings
from users.models import CustomUser


class Topic(models.Model):
    """用户看到的校园墙主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
    
class Entry(models.Model):
    """某个主题下的具体内容"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_entries')
    is_read = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串显示"""
        if len(self.text)>50:
            return f"{self.text[:50]}..."
        else:
            return self.text
    
class Reply(models.Model):
    """某条帖子下的回复"""
    entry = models.ForeignKey(Entry,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_replies')
    is_read = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'replies'

    def __str__(self):
        """返回模型的字符串显示"""
        if len(self.text)>50:
            return f"{self.text[:50]}..."
        else:
            return self.text

