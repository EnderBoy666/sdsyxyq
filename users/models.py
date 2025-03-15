from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 添加自定义字段
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 允许 NULL
    introduction = models.CharField(max_length=400, blank=True, default='这个家伙很懒，还没有添加简介~~')
